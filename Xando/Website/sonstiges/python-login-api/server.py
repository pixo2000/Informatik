from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email configuration
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")
recipient_email = os.getenv("RECIPIENT_EMAIL")

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a directory for storing form submissions
SUBMISSIONS_DIR = "submissions"
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

# Email functions
def send_test_email():
    """Send a test email to verify email configuration."""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Test Email from Python Script"
    
    body = """
    Hello,
    
    This is a test email sent from a Python script.
    
    Best regards,
    Python Email Test Script
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"Test email successfully sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_confirmation_email(customer_email, form_data):
    """Send a confirmation email to the customer with their form data."""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Bestätigung Ihrer Anfrage"
    
    # Build email body with form data
    name = f"{form_data.get('vorname', '')} {form_data.get('nachname', '')}"
    address = f"{form_data.get('strasse', '')} {form_data.get('hausnr', '')}, {form_data.get('plz', '')} {form_data.get('ort', '')}"
    products = ", ".join(form_data.get('produkt', [])) if isinstance(form_data.get('produkt'), list) else form_data.get('produkt', 'Keine')
    shipping_method = form_data.get('bestellmethode', 'Nicht angegeben')
    payment_method = form_data.get('zahlungsmethode', 'Nicht angegeben')
    
    body = f"""
    Hallo {name},
    
    vielen Dank für Ihre Anfrage. Hier ist eine Zusammenfassung Ihrer Daten:
    
    Name: {name}
    E-Mail: {form_data.get('email', '')}
    Adresse: {address}
    Land: {form_data.get('land', '')}
    Datum: {form_data.get('datum', '')}
    
    Produktkategorie: {products}
    Bestellmethode: {shipping_method}
    Zahlungsmethode: {payment_method}
    
    Wir werden Ihre Anfrage so schnell wie möglich bearbeiten.
    
    Mit freundlichen Grüßen,
    Ihr Support-Team
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"Confirmation email successfully sent to {customer_email}")
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False

# API Routes
@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data from request
        form_data = request.json
        
        # Validate required fields
        if not form_data.get('email'):
            return jsonify({"success": False, "message": "Email is required"}), 400
        
        # Generate timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{form_data.get('nachname', 'unknown')}.txt"
        file_path = os.path.join(SUBMISSIONS_DIR, filename)
        
        # Save form data to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(form_data, indent=4, ensure_ascii=False))
        
        # Send confirmation email to customer
        customer_email = form_data.get('email')
        email_sent = send_confirmation_email(customer_email, form_data)
        
        if not email_sent:
            return jsonify({
                "success": True, 
                "message": "Form submitted but could not send confirmation email"
            })
        
        return jsonify({"success": True, "message": "Form submitted successfully"})
    
    except Exception as e:
        print(f"Error processing form submission: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

# Test endpoint to verify the server is running
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "Server is running"})

if __name__ == "__main__":
    # You can uncomment this to test email functionality separately
    # send_test_email()
    print("Starting server on http://localhost:5000")
    app.run(debug=False, port=5000)
