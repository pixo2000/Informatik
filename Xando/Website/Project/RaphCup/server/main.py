from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

# Import our modules
from config import SECURITY_CONFIG, SERVER_CONFIG
from database import db
from email_service import email_service
from auth import (generate_verification_code, generate_reset_token, 
                  get_verification_expiry, get_reset_expiry, is_expired,
                  require_auth, require_admin)

app = Flask(__name__, static_folder='../client', template_folder='../client')
CORS(app)
app.secret_key = SECURITY_CONFIG['secret_key']

# Routes for serving HTML pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user = db.get_user_by_email(session.get('email', ''))
    if not user or not user[7]:  # is_admin column
        return redirect(url_for('dashboard'))
    
    return render_template('admin.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Check if user exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    # Create user
    hashed_password = generate_password_hash(password)
    verification_code = generate_verification_code()
    verification_expires = get_verification_expiry().isoformat()
    
    user_id = db.create_user(email, hashed_password, verification_code, verification_expires)
    if not user_id:
        return jsonify({'error': 'Registration failed'}), 500
    
    # Send verification email
    if email_service.send_verification_email(email, verification_code):
        return jsonify({'message': 'Registration successful. Please check your email for verification code.'})
    else:
        return jsonify({'error': 'Failed to send verification email. Please try again.'}), 500

@app.route('/api/verify', methods=['POST'])
def verify_email():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    
    if not email or not code:
        return jsonify({'error': 'Email and verification code required'}), 400
    
    user = db.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check verification code and expiry
    if user[4] != code.upper():  # verification_code column
        return jsonify({'error': 'Invalid verification code'}), 400
    
    if is_expired(user[5]):  # verification_expires column
        return jsonify({'error': 'Verification code has expired. Please register again.'}), 400
    
    # Verify user
    db.verify_user(email)
    
    return jsonify({'message': 'Email verified successfully. You can now log in.'})

@app.route('/api/resend-verification', methods=['POST'])
def resend_verification():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    user = db.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user[3]:  # verified column
        return jsonify({'error': 'Email is already verified'}), 400
    
    # Generate new verification code
    verification_code = generate_verification_code()
    verification_expires = get_verification_expiry().isoformat()
    
    # Update user with new code
    conn = db.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET verification_code = ?, verification_expires = ? WHERE email = ?',
              (verification_code, verification_expires, email))
    conn.commit()
    conn.close()
    
    # Send new verification email
    if email_service.send_verification_email(email, verification_code):
        return jsonify({'message': 'New verification code sent to your email.'})
    else:
        return jsonify({'error': 'Failed to send verification email.'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = db.get_user_by_email(email)
    if not user or not check_password_hash(user[2], password):  # password column
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user[3]:  # verified column
        return jsonify({'error': 'Please verify your email first'}), 401
    
    # Set session
    session['user_id'] = user[0]
    session['email'] = user[1]
    session['is_admin'] = user[7]  # is_admin column
    
    return jsonify({
        'message': 'Login successful', 
        'is_admin': user[7],
        'user_id': user[0]
    })

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    user = db.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user[3]:  # verified column
        return jsonify({'error': 'Please verify your email first'}), 400
    
    # Generate reset token
    reset_token = generate_reset_token()
    reset_expires = get_reset_expiry().isoformat()
    
    # Save reset token
    db.set_reset_token(email, reset_token, reset_expires)
    
    # Send reset email
    if email_service.send_password_reset_email(email, reset_token):
        return jsonify({'message': 'Password reset link sent to your email.'})
    else:
        return jsonify({'error': 'Failed to send reset email.'}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    user = db.get_user_by_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid reset token'}), 400
    
    if is_expired(user[8]):  # reset_expires column
        return jsonify({'error': 'Reset token has expired'}), 400
    
    # Update password
    new_password_hash = generate_password_hash(new_password)
    db.update_password(user[0], new_password_hash)
    
    return jsonify({'message': 'Password reset successfully. You can now log in with your new password.'})

@app.route('/api/tournaments', methods=['GET'])
def get_tournaments():
    tournaments = db.get_tournaments()
    
    return jsonify([{
        'id': t[0], 'name': t[1], 'description': t[2],
        'date1': t[3], 'date2': t[4], 'final_date': t[5],
        'registration_deadline': t[6], 'max_players': t[7],
        'status': t[9], 'created_at': t[10]
    } for t in tournaments])

@app.route('/api/tournaments', methods=['POST'])
@require_admin
def create_tournament():
    data = request.json
    
    required_fields = ['name', 'description', 'date1', 'date2', 'registration_deadline', 'max_players']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    tournament_id = db.create_tournament(
        data['name'], data['description'], data['date1'], data['date2'],
        data['registration_deadline'], data['max_players'], session['user_id']
    )
    
    if tournament_id:
        return jsonify({'message': 'Tournament created successfully', 'tournament_id': tournament_id})
    else:
        return jsonify({'error': 'Failed to create tournament'}), 500

@app.route('/api/register_tournament', methods=['POST'])
@require_auth
def register_for_tournament():
    data = request.json
    
    required_fields = ['tournament_id', 'discord_tag', 'valorant_rank', 'valorant_peak', 'date_vote']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Update user profile
    db.update_user_profile(
        session['user_id'], 
        data['discord_tag'], 
        data['valorant_rank'], 
        data['valorant_peak']
    )
    
    # Register for tournament
    success = db.register_for_tournament(
        data['tournament_id'], 
        session['user_id'], 
        data['date_vote']
    )
    
    if success:
        return jsonify({'message': 'Successfully registered for tournament'})
    else:
        return jsonify({'error': 'Registration failed. You may already be registered for this tournament.'}), 400

@app.route('/api/user/tournaments', methods=['GET'])
@require_auth
def get_user_tournaments():
    conn = db.get_connection()
    c = conn.cursor()
    c.execute('''SELECT t.*, r.date_vote, r.registered_at 
                 FROM tournaments t 
                 JOIN registrations r ON t.id = r.tournament_id 
                 WHERE r.user_id = ?
                 ORDER BY r.registered_at DESC''', (session['user_id'],))
    user_tournaments = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': t[0], 'name': t[1], 'description': t[2],
        'date1': t[3], 'date2': t[4], 'final_date': t[5],
        'registration_deadline': t[6], 'max_players': t[7],
        'status': t[9], 'date_vote': t[11], 'registered_at': t[12]
    } for t in user_tournaments])

@app.route('/api/admin/registrations/<int:tournament_id>', methods=['GET'])
@require_admin
def get_tournament_registrations(tournament_id):
    conn = db.get_connection()
    c = conn.cursor()
    c.execute('''SELECT u.email, u.discord_tag, u.valorant_rank, u.valorant_peak, 
                        r.date_vote, r.registered_at
                 FROM registrations r
                 JOIN users u ON r.user_id = u.id
                 WHERE r.tournament_id = ?
                 ORDER BY r.registered_at''', (tournament_id,))
    registrations = c.fetchall()
    conn.close()
    
    return jsonify([{
        'email': r[0], 'discord_tag': r[1], 'valorant_rank': r[2],
        'valorant_peak': r[3], 'date_vote': r[4], 'registered_at': r[5]
    } for r in registrations])

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_user_profile():
    user = db.get_user_by_email(session['email'])
    if user:
        return jsonify({
            'email': user[1],
            'discord_tag': user[8],
            'valorant_rank': user[9],
            'valorant_peak': user[10],
            'is_admin': user[7]
        })
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(
        debug=SERVER_CONFIG['debug'], 
        host=SERVER_CONFIG['host'], 
        port=SERVER_CONFIG['port']
    )
