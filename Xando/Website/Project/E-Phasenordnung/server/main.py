from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import shutil
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data file paths
DATA_FILE = 'students.json'
ASSIGNMENTS_FILE = 'assignments.json'
BACKUP_DIR = 'backups'

# Create backup directory if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Auto-backup settings
BACKUP_INTERVAL = 300  # 5 minutes in seconds
last_backup_time = 0

def load_students():
    """Load students from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Fehler beim Laden der Schülerdaten: {e}")
            # Try to load from latest backup
            return load_from_backup('students')
    return []

def save_students(students):
    """Save students to JSON file with automatic backup"""
    try:
        # Create backup before saving
        create_backup()
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(students, f, ensure_ascii=False, indent=2)
        print(f"✅ Schülerdaten gespeichert: {len(students)} Schüler")
        return True
    except IOError as e:
        print(f"❌ Fehler beim Speichern der Schülerdaten: {e}")
        return False

def load_assignments():
    """Load assignments from JSON file"""
    if os.path.exists(ASSIGNMENTS_FILE):
        try:
            with open(ASSIGNMENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Fehler beim Laden der Zuordnungen: {e}")
            return load_from_backup('assignments')
    return None

def save_assignments(assignments):
    """Save assignments to JSON file with automatic backup"""
    try:
        # Create backup before saving
        create_backup()
        
        with open(ASSIGNMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(assignments, f, ensure_ascii=False, indent=2)
        print(f"✅ Klassenzuordnungen gespeichert")
        return True
    except IOError as e:
        print(f"❌ Fehler beim Speichern der Zuordnungen: {e}")
        return False

def create_backup():
    """Create backup of all data files"""
    global last_backup_time
    current_time = time.time()
    
    # Only create backup if enough time has passed
    if current_time - last_backup_time < BACKUP_INTERVAL:
        return
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Backup students data
        if os.path.exists(DATA_FILE):
            backup_file = os.path.join(BACKUP_DIR, f'students_{timestamp}.json')
            shutil.copy2(DATA_FILE, backup_file)
            print(f"📁 Backup erstellt: {backup_file}")
        
        # Backup assignments data
        if os.path.exists(ASSIGNMENTS_FILE):
            backup_file = os.path.join(BACKUP_DIR, f'assignments_{timestamp}.json')
            shutil.copy2(ASSIGNMENTS_FILE, backup_file)
            print(f"📁 Backup erstellt: {backup_file}")
        
        # Clean old backups (keep only last 10)
        clean_old_backups()
        
        last_backup_time = current_time
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Backups: {e}")

def load_from_backup(data_type):
    """Load data from the most recent backup"""
    try:
        backup_files = [f for f in os.listdir(BACKUP_DIR) if f.startswith(f'{data_type}_') and f.endswith('.json')]
        if not backup_files:
            print(f"⚠️ Keine Backups für {data_type} gefunden")
            return [] if data_type == 'students' else None
        
        # Sort by timestamp (newest first)
        backup_files.sort(reverse=True)
        latest_backup = os.path.join(BACKUP_DIR, backup_files[0])
        
        with open(latest_backup, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"🔄 Daten aus Backup wiederhergestellt: {latest_backup}")
        return data
        
    except Exception as e:
        print(f"❌ Fehler beim Laden des Backups: {e}")
        return [] if data_type == 'students' else None

def clean_old_backups():
    """Keep only the 10 most recent backups"""
    try:
        for data_type in ['students', 'assignments']:
            backup_files = [f for f in os.listdir(BACKUP_DIR) if f.startswith(f'{data_type}_') and f.endswith('.json')]
            backup_files.sort(reverse=True)  # Newest first
            
            # Remove old backups (keep only 10)
            for old_backup in backup_files[10:]:
                old_backup_path = os.path.join(BACKUP_DIR, old_backup)
                os.remove(old_backup_path)
                print(f"🗑️ Altes Backup entfernt: {old_backup}")
                
    except Exception as e:
        print(f"❌ Fehler beim Aufräumen der Backups: {e}")

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = load_students()
    # Sort by priority (highest first)
    students.sort(key=lambda x: x.get('prioritaet', 0), reverse=True)
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    """Add a new student"""
    try:
        student_data = request.json
        
        # Validate required fields
        required_fields = ['nachname', 'vorname', 'geschlecht', 'zweiteFremdsprache', 
                          'musischesFach', 'religioesesFach', 'freiesFach']
        
        for field in required_fields:
            if not student_data.get(field):
                return jsonify({'error': f'Feld {field} ist erforderlich'}), 400
          # Load existing students
        students = load_students()
        
        # Check for duplicate names
        nachname = student_data.get('nachname', '').strip()
        vorname = student_data.get('vorname', '').strip()
        
        duplicate = next((s for s in students 
                         if s.get('nachname', '').lower() == nachname.lower() 
                         and s.get('vorname', '').lower() == vorname.lower()), None)
        
        if duplicate:
            return jsonify({'error': f'Ein Schüler mit dem Namen "{vorname} {nachname}" existiert bereits'}), 409
        
        # Generate new ID if not provided
        if 'id' not in student_data:
            student_data['id'] = int(datetime.now().timestamp() * 1000)
        
        # Set creation timestamp
        student_data['erstelltAm'] = datetime.now().isoformat()
        
        # Calculate priority
        student_data['prioritaet'] = calculate_priority(student_data)
        
        # Add student
        students.append(student_data)
        
        # Save to file
        if save_students(students):
            return jsonify(student_data), 201
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update an existing student"""
    try:
        student_data = request.json
        students = load_students()
        
        # Find student index
        student_index = next((i for i, s in enumerate(students) if s['id'] == student_id), None)
        if student_index is None:
            return jsonify({'error': 'Schüler nicht gefunden'}), 404
        
        # Check for duplicate names (exclude current student)
        nachname = student_data.get('nachname', '').strip()
        vorname = student_data.get('vorname', '').strip()
        
        duplicate = next((s for s in students 
                         if s.get('id') != student_id
                         and s.get('nachname', '').lower() == nachname.lower() 
                         and s.get('vorname', '').lower() == vorname.lower()), None)
        
        if duplicate:
            return jsonify({'error': f'Ein anderer Schüler mit dem Namen "{vorname} {nachname}" existiert bereits'}), 409
        
        # Update student data
        student_data['id'] = student_id
        student_data['prioritaet'] = calculate_priority(student_data)
        students[student_index] = student_data
        
        # Save to file
        if save_students(students):
            return jsonify(student_data)
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        students = load_students()
        
        # Find and remove student
        original_length = len(students)
        students = [s for s in students if s['id'] != student_id]
        
        if len(students) == original_length:
            return jsonify({'error': 'Schüler nicht gefunden'}), 404
        
        # Save to file
        if save_students(students):
            return jsonify({'message': 'Schüler erfolgreich gelöscht'})
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/stats', methods=['GET'])
def get_stats():
    """Get statistics about students"""
    students = load_students()
    
    stats = {
        'total': len(students),
        'rechtzeitigAbgegeben': len([s for s in students if s.get('rechtzeitigAbgegeben', False)]),
        'geschlecht': {},
        'zweiteFremdsprache': {},
        'averagePriority': 0
    }
    
    if students:
        # Count by gender
        for student in students:
            gender = student.get('geschlecht', 'Unbekannt')
            stats['geschlecht'][gender] = stats['geschlecht'].get(gender, 0) + 1
        
        # Count by second language
        for student in students:
            lang = student.get('zweiteFremdsprache', 'Unbekannt')
            stats['zweiteFremdsprache'][lang] = stats['zweiteFremdsprache'].get(lang, 0) + 1
        
        # Calculate average priority
        total_priority = sum(s.get('prioritaet', 0) for s in students)
        stats['averagePriority'] = round(total_priority / len(students), 2)
    
    return jsonify(stats)

@app.route('/api/assignments', methods=['POST'])
def create_class_assignments():
    """Create automatic class assignments"""
    try:
        data = request.json
        number_of_classes = data.get('numberOfClasses', 3)
        
        if number_of_classes < 1 or number_of_classes > 10:
            return jsonify({'error': 'Anzahl der Klassen muss zwischen 1 und 10 liegen'}), 400
        
        students = load_students()
        
        if len(students) < number_of_classes:
            return jsonify({'error': 'Es müssen mindestens so viele Schüler wie Klassen vorhanden sein'}), 400
        
        # Create assignments using the same algorithm as frontend
        assignments = create_assignments_algorithm(students, number_of_classes)
          # Save assignments to file
        assignment_data = {
            'timestamp': datetime.now().isoformat(),
            'numberOfClasses': number_of_classes,
            'totalStudents': len(students),
            'assignments': assignments
        }
        
        save_assignments(assignment_data)
        
        return jsonify(assignment_data), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignments', methods=['GET'])
def get_latest_assignments():
    """Get the latest class assignments"""
    try:
        assignments = load_assignments()
        if assignments:
            return jsonify(assignments)
        else:
            return jsonify({'error': 'Keine Zuordnungen gefunden'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignments', methods=['PUT'])
def update_class_assignments():
    """Update class assignments manually"""
    try:
        assignment_data = request.json
        
        # Validate that all students are assigned
        students = load_students()
        student_ids = {s['id'] for s in students}
        assigned_ids = set()
        
        for class_obj in assignment_data.get('assignments', []):
            for student in class_obj.get('students', []):
                assigned_ids.add(student.get('id'))
        
        # Check if all students are assigned
        if student_ids != assigned_ids:
            missing = student_ids - assigned_ids
            extra = assigned_ids - student_ids
            error_msg = ""
            if missing:
                error_msg += f"Fehlende Schüler-IDs: {missing}. "
            if extra:
                error_msg += f"Unbekannte Schüler-IDs: {extra}. "
            return jsonify({'error': error_msg}), 400
        
        # Update timestamp and save
        assignment_data['timestamp'] = assignment_data.get('timestamp', datetime.now().isoformat())
        assignment_data['lastModified'] = datetime.now().isoformat()
        assignment_data['manuallyEdited'] = True
        
        if save_assignments(assignment_data):
            return jsonify(assignment_data)
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignments', methods=['DELETE'])
def delete_assignments():
    """Delete all class assignments"""
    try:
        if os.path.exists(ASSIGNMENTS_FILE):
            os.remove(ASSIGNMENTS_FILE)
            print("🗑️ Klassenzuordnungen gelöscht")
        return jsonify({'message': 'Klassenzuordnungen erfolgreich gelöscht'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignments/student/<int:student_id>/move', methods=['POST'])
def move_student_to_class(student_id):
    """Move a student from one class to another"""
    try:
        data = request.json
        target_class_id = data.get('targetClassId')
        
        if target_class_id is None:
            return jsonify({'error': 'targetClassId ist erforderlich'}), 400
        
        assignments = load_assignments()
        if not assignments:
            return jsonify({'error': 'Keine Zuordnungen gefunden'}), 404
        
        # Find and remove student from current class
        student_found = False
        student_data = None
        
        for class_obj in assignments['assignments']:
            students_to_keep = []
            for student in class_obj['students']:
                if student['id'] == student_id:
                    student_found = True
                    student_data = student
                else:
                    students_to_keep.append(student)
            class_obj['students'] = students_to_keep
        
        if not student_found:
            return jsonify({'error': 'Schüler nicht gefunden'}), 404
        
        # Find target class and add student
        target_class_found = False
        for class_obj in assignments['assignments']:
            if class_obj['id'] == target_class_id:
                class_obj['students'].append(student_data)
                target_class_found = True
                break
        
        if not target_class_found:
            return jsonify({'error': 'Zielklasse nicht gefunden'}), 404
        
        # Update stats for all classes
        for class_obj in assignments['assignments']:
            update_class_stats(class_obj)
        
        # Mark as manually edited and save
        assignments['lastModified'] = datetime.now().isoformat()
        assignments['manuallyEdited'] = True
        
        if save_assignments(assignments):
            return jsonify(assignments)
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_class_stats(class_obj):
    """Update statistics for a class"""
    class_obj['stats'] = {
        'männlich': 0,
        'weiblich': 0,
        'subjects': {}
    }
    
    for student in class_obj['students']:
        # Update gender count
        gender = student.get('geschlecht', 'Unbekannt')
        if gender in class_obj['stats']:
            class_obj['stats'][gender] += 1
        
        # Update subject count
        subjects = [
            student.get('zweiteFremdsprache'),
            student.get('musischesFach'),
            student.get('religioesesFach'),
            student.get('freiesFach')
        ]
        
        for subject in subjects:
            if subject:
                if subject not in class_obj['stats']['subjects']:
                    class_obj['stats']['subjects'][subject] = 0
                class_obj['stats']['subjects'][subject] += 1

def create_assignments_algorithm(students, number_of_classes):
    """Server-side implementation of class assignment algorithm"""
    # Sort students by priority
    sorted_students = sorted(students, key=lambda x: x.get('prioritaet', 0), reverse=True)
    
    # Initialize classes
    classes = []
    for i in range(number_of_classes):
        classes.append({
            'id': i + 1,
            'name': f'Klasse {i + 1}',
            'students': [],
            'stats': {
                'männlich': 0,
                'weiblich': 0,
                'subjects': {}
            }
        })
    
    # Simple round-robin assignment with gender balance consideration
    for i, student in enumerate(sorted_students):
        # Find class with best gender balance
        best_class_idx = 0
        best_balance = float('inf')
        
        for j, class_obj in enumerate(classes):
            current_male = class_obj['stats']['männlich']
            current_female = class_obj['stats']['weiblich']
            total = current_male + current_female
            
            if total == 0:
                balance_score = 0
            else:
                # Calculate how balanced the class would be after adding this student
                if student['geschlecht'] == 'männlich':
                    new_male = current_male + 1
                    new_female = current_female
                else:
                    new_male = current_male
                    new_female = current_female + 1
                
                new_total = new_male + new_female
                balance_score = abs(new_male - new_female) / new_total
            
            # Also consider class size
            size_penalty = len(class_obj['students']) * 0.1
            total_score = balance_score + size_penalty
            
            if total_score < best_balance:
                best_balance = total_score
                best_class_idx = j
        
        # Assign student to best class
        classes[best_class_idx]['students'].append(student)
        classes[best_class_idx]['stats'][student['geschlecht']] += 1
        
        # Update subject stats
        subjects = [student.get('zweiteFremdsprache'), student.get('musischesFach'), 
                   student.get('religioesesFach'), student.get('freiesFach')]
        for subject in subjects:
            if subject:
                if subject not in classes[best_class_idx]['stats']['subjects']:
                    classes[best_class_idx]['stats']['subjects'][subject] = 0
                classes[best_class_idx]['stats']['subjects'][subject] += 1
    
    return classes

def calculate_priority(student_data):
    """Calculate student priority based on fields"""
    priority = 1
    
    # Rechtzeitig abgegeben hat höchste Priorität
    if student_data.get('rechtzeitigAbgegeben', False):
        priority += 100
    
    # Andere Felder haben abnehmende Priorität
    field_priorities = {
        'zweiteFremdsprache': 90,
        'musischesFach': 80,
        'religioesesFach': 70,
        'freiesFach': 60,
        'freund1': 50,
        'freund2': 40
    }
    
    for field, points in field_priorities.items():
        if student_data.get(field) and str(student_data[field]).strip():
            priority += points
    
    return priority

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint nicht gefunden'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Interner Server-Fehler'}), 500

if __name__ == '__main__':
    print("🚀 E-Phasen API Server gestartet")
    print("📊 Endpunkte:")
    print("   GET    /api/students           - Alle Schüler abrufen")
    print("   POST   /api/students           - Neuen Schüler hinzufügen")
    print("   PUT    /api/students/<id>      - Schüler aktualisieren")
    print("   DELETE /api/students/<id>      - Schüler löschen")
    print("   GET    /api/students/stats     - Statistiken abrufen")
    print("   POST   /api/assignments        - Klassenzuordnung erstellen")
    print("   GET    /api/assignments        - Letzte Zuordnung abrufen")
    print("   PUT    /api/assignments        - Klassenzuordnung manuell bearbeiten")
    print("   DELETE /api/assignments        - Klassenzuordnungen löschen")
    print("   POST   /api/assignments/student/<id>/move - Schüler zwischen Klassen verschieben")
    print("   GET    /api/health             - Health Check")
    print()
    print("🌐 Server läuft auf: http://localhost:5000")
    print("📝 Daten werden gespeichert in: students.json, assignments.json")
    print("💾 Automatische Backups in: backups/ (alle 5 Minuten)")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)