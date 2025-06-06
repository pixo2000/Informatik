// Global variables
let students = [];
let currentEditId = null;
let classAssignments = [];

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api'; // Adjust this to your server URL

// Load data from server on page load
document.addEventListener('DOMContentLoaded', function() {
    loadStudentsFromServer();
    updateStudentCount();
      // Setup form submission
    document.getElementById('studentForm').addEventListener('submit', handleFormSubmit);
    
    // Setup validation for special subject combinations
    document.getElementById('zweiteFremdsprache').addEventListener('change', validateSubjectCombinations);
    document.getElementById('freiesFach').addEventListener('change', validateSubjectCombinations);
    
    // Setup real-time name validation
    document.getElementById('nachname').addEventListener('input', validateNameUniqueness);
    document.getElementById('vorname').addEventListener('input', validateNameUniqueness);
    
    // Prevent default dragover behavior on document
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    // Clean up drag states when drag ends
    document.addEventListener('dragend', function(e) {
        document.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
        document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    });
    
    // Warn about unsaved changes before leaving page
    window.addEventListener('beforeunload', function(e) {
        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = 'Sie haben ungespeicherte Änderungen. Möchten Sie die Seite wirklich verlassen?';
        }
    });
    
    // Setup assignment button event listeners
    const assignBtn = document.getElementById('assignClassesBtn');
    const resetBtn = document.getElementById('resetAssignmentsBtn');
    
    if (assignBtn) {
        assignBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            assignClasses();
        });
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            resetClassAssignments();
        });
    }
});

// Toggle date input based on checkbox
function toggleDateInput() {
    const checkbox = document.getElementById('rechtzeitigAbgegeben');
    const dateContainer = document.getElementById('dateInputContainer');
    
    if (checkbox.checked) {
        dateContainer.style.display = 'none';
        document.getElementById('abgabedatum').value = '';
    } else {
        dateContainer.style.display = 'block';
        // Set today's date as default for late submission
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('abgabedatum').value = today;
    }
}

// Tab switching functionality
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Add active class to the correct button based on tab name
    const tabMapping = {
        'input': 0,
        'overview': 1,
        'classes': 2
    };
    
    const buttons = document.querySelectorAll('.tab-btn');
    if (buttons[tabMapping[tabName]]) {
        buttons[tabMapping[tabName]].classList.add('active');
    }
    
    // Update student count when switching to overview
    if (tabName === 'overview') {
        updateStudentCount();
        renderStudentsTable();
    }
}

// Form submission handler
function handleFormSubmit(event) {
    event.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    const formData = new FormData(event.target);
    const studentData = {
        id: currentEditId || Date.now(),        nachname: formData.get('nachname').trim(),
        vorname: formData.get('vorname').trim(),
        geschlecht: formData.get('geschlecht'),
        externerSchueler: formData.get('externerSchueler') === 'on',
        rechtzeitigAbgegeben: formData.get('rechtzeitigAbgegeben') === 'on',
        abgabedatum: formData.get('abgabedatum') || null,
        zweiteFremdsprache: formData.get('zweiteFremdsprache'),
        musischesFach: formData.get('musischesFach'),
        religioesesFach: formData.get('religioesesFach'),
        freiesFach: formData.get('freiesFach'),
        freund1: formData.get('freund1').trim(),
        freund2: formData.get('freund2').trim(),
        erstelltAm: currentEditId ? findStudentById(currentEditId).erstelltAm : new Date().toISOString(),
        // Priorität basierend auf Position nach Abgabedatum und Abgabedatum selbst
        prioritaet: calculatePriority(formData)
    };
    
    if (currentEditId) {
        updateStudentOnServer(studentData);
    } else {
        addStudentToServer(studentData);
    }
}

// Calculate priority based on field order after "rechtzeitigAbgegeben" and submission date
function calculatePriority(formData) {
    let priority = 1;
    
    // Rechtzeitig abgegeben hat höchste Priorität
    if (formData.get('rechtzeitigAbgegeben') === 'on') {
        priority += 100;
    } else {
        // Spät abgegebene haben niedrigere Priorität basierend auf Abgabedatum
        const abgabedatum = formData.get('abgabedatum');
        if (abgabedatum) {
            const submissionDate = new Date(abgabedatum);
            const today = new Date();
            const daysDifference = Math.ceil((today - submissionDate) / (1000 * 60 * 60 * 24));
            
            // Je später, desto niedriger die Priorität
            priority += Math.max(50 - daysDifference * 5, 10);
        } else {
            priority += 30; // Mittlere Priorität wenn kein Datum angegeben
        }
    }
    
    // Andere Felder haben abnehmende Priorität
    const fieldPriorities = {
        'zweiteFremdsprache': 90,
        'musischesFach': 80,
        'religioesesFach': 70,
        'freiesFach': 60,
        'freund1': 50,
        'freund2': 40
    };
    
    Object.entries(fieldPriorities).forEach(([field, points]) => {
        if (formData.get(field) && formData.get(field).trim()) {
            priority += points;
        }
    });
    
    return priority;
}

// Form validation
function validateForm() {
    const form = document.getElementById('studentForm');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        field.classList.remove('error');
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        }
    });
      if (!isValid) {
        showNotification('Bitte füllen Sie alle Pflichtfelder aus!', 'error');
        return false;
    }
    
    // Check for duplicate names (only when adding new student, not when editing)
    if (!currentEditId) {
        const nachname = document.getElementById('nachname').value.trim();
        const vorname = document.getElementById('vorname').value.trim();
        
        const duplicate = students.find(student => 
            student.nachname.toLowerCase() === nachname.toLowerCase() && 
            student.vorname.toLowerCase() === vorname.toLowerCase()
        );
        
        if (duplicate) {
            showNotification(`Ein Schüler mit dem Namen "${vorname} ${nachname}" existiert bereits!`, 'error');
            document.getElementById('nachname').classList.add('error');
            document.getElementById('vorname').classList.add('error');
            return false;
        }
    }
    
    // Validate subject combinations
    const zweiteFremdsprache = document.getElementById('zweiteFremdsprache').value;
    const freiesFach = document.getElementById('freiesFach').value;
    
    if (freiesFach === 'Spanisch (3. Fremdsprache)' && zweiteFremdsprache === 'Spanisch') {
        showNotification('Spanisch kann nicht gleichzeitig 2. und 3. Fremdsprache sein!', 'error');
        return false;
    }
    
    if (freiesFach === 'Latein (3. Fremdsprache)' && zweiteFremdsprache === 'Latein') {
        showNotification('Latein kann nicht gleichzeitig 2. und 3. Fremdsprache sein!', 'error');
        return false;
    }
    
    return true;
}

// Validate subject combinations in real-time
function validateSubjectCombinations() {
    const zweiteFremdsprache = document.getElementById('zweiteFremdsprache').value;
    const freiesFach = document.getElementById('freiesFach').value;
    const freiesFachSelect = document.getElementById('freiesFach');
    
    // Reset options
    Array.from(freiesFachSelect.options).forEach(option => {
        option.disabled = false;
        option.style.color = '';
    });
    
    // Disable conflicting options
    if (zweiteFremdsprache === 'Spanisch') {
        const spanishOption = freiesFachSelect.querySelector('option[value="Spanisch (3. Fremdsprache)"]');
        if (spanishOption) {
            spanishOption.disabled = true;
            spanishOption.style.color = '#ccc';
        }
        if (freiesFach === 'Spanisch (3. Fremdsprache)') {
            freiesFachSelect.value = '';
        }
    }
    
    if (zweiteFremdsprache === 'Latein') {
        const latinOption = freiesFachSelect.querySelector('option[value="Latein (3. Fremdsprache)"]');
        if (latinOption) {
            latinOption.disabled = true;
            latinOption.style.color = '#ccc';
        }
        if (freiesFach === 'Latein (3. Fremdsprache)') {
            freiesFachSelect.value = '';
        }    }
}

// Real-time name validation
function validateNameUniqueness() {
    // Only validate when adding new student, not when editing
    if (currentEditId) return;
    
    const nachnameField = document.getElementById('nachname');
    const vornameField = document.getElementById('vorname');
    const nachname = nachnameField.value.trim();
    const vorname = vornameField.value.trim();
    
    // Clear previous error states
    nachnameField.classList.remove('error');
    vornameField.classList.remove('error');
    
    // Only check if both fields have values
    if (nachname && vorname) {
        const duplicate = students.find(student => 
            student.nachname.toLowerCase() === nachname.toLowerCase() && 
            student.vorname.toLowerCase() === vorname.toLowerCase()
        );
        
        if (duplicate) {
            nachnameField.classList.add('error');
            vornameField.classList.add('error');
            
            // Show warning message
            let existingWarning = document.querySelector('.name-duplicate-warning');
            if (!existingWarning) {
                const warning = document.createElement('div');
                warning.className = 'name-duplicate-warning';
                warning.style.cssText = `
                    color: #dc3545;
                    font-size: 0.9rem;
                    margin-top: 5px;
                    padding: 8px 12px;
                    background: rgba(220, 53, 69, 0.1);
                    border: 1px solid rgba(220, 53, 69, 0.3);
                    border-radius: 4px;
                `;
                warning.innerHTML = `⚠️ Ein Schüler mit dem Namen "${vorname} ${nachname}" existiert bereits!`;
                
                // Insert after the second form-group in the first form-row
                const firstFormRow = document.querySelector('.form-row');
                firstFormRow.appendChild(warning);
            } else {
                existingWarning.innerHTML = `⚠️ Ein Schüler mit dem Namen "${vorname} ${nachname}" existiert bereits!`;
            }
        } else {
            // Remove warning if names are unique
            const existingWarning = document.querySelector('.name-duplicate-warning');
            if (existingWarning) {
                existingWarning.remove();
            }
        }
    } else {
        // Remove warning if fields are empty
        const existingWarning = document.querySelector('.name-duplicate-warning');
        if (existingWarning) {
            existingWarning.remove();
        }
    }
}

// Reset form
function resetForm() {
    document.getElementById('studentForm').reset();
    currentEditId = null;
    document.querySelector('.form-actions button[type="submit"]').textContent = 'Schüler hinzufügen';
    
    // Remove all error classes
    document.querySelectorAll('.error').forEach(field => {
        field.classList.remove('error');
    });
    
    // Remove name duplicate warning
    const existingWarning = document.querySelector('.name-duplicate-warning');
    if (existingWarning) {
        existingWarning.remove();
    }
    
    // Reset subject combinations
    validateSubjectCombinations();
}

// Search functionality
function searchStudents() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    renderStudentsTable(searchTerm);
}

// Filter functionality
function filterStudents() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    renderStudentsTable(searchTerm);
}

// Clear all filters
function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('genderFilter').value = '';
    document.getElementById('languageFilter').value = '';
    renderStudentsTable();
}

// Render students table
function renderStudentsTable(searchTerm = '') {
    const tbody = document.getElementById('studentsTableBody');
    const genderFilter = document.getElementById('genderFilter').value;
    const languageFilter = document.getElementById('languageFilter').value;
    
    let filteredStudents = students.filter(student => {
        const matchesSearch = !searchTerm || 
            student.nachname.toLowerCase().includes(searchTerm) ||
            student.vorname.toLowerCase().includes(searchTerm) ||
            student.zweiteFremdsprache.toLowerCase().includes(searchTerm) ||
            student.musischesFach.toLowerCase().includes(searchTerm) ||
            student.religioesesFach.toLowerCase().includes(searchTerm) ||
            student.freiesFach.toLowerCase().includes(searchTerm) ||
            student.freund1.toLowerCase().includes(searchTerm) ||
            student.freund2.toLowerCase().includes(searchTerm);
            
        const matchesGender = !genderFilter || student.geschlecht === genderFilter;
        const matchesLanguage = !languageFilter || student.zweiteFremdsprache === languageFilter;
        
        return matchesSearch && matchesGender && matchesLanguage;
    });
    
    // Sort by priority (highest first)
    filteredStudents.sort((a, b) => (b.prioritaet || 0) - (a.prioritaet || 0));
      if (filteredStudents.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="10" class="empty-state">
                    <p>Keine Schüler gefunden.</p>
                    ${students.length === 0 ? '<button onclick="showTab(\'input\')">Ersten Schüler hinzufügen</button>' : ''}
                </td>
            </tr>
        `;
        updateStudentCount(0);
        return;
    }
      tbody.innerHTML = filteredStudents.map((student, index) => `
        <tr>
            <td>
                <strong>${student.nachname}, ${student.vorname}</strong>
                <small style="display: block; color: #666; font-size: 0.8em;">
                    Priorität: ${student.prioritaet || 0} (#${index + 1})
                </small>
            </td>
            <td>${student.geschlecht}</td>
            <td>
                <span class="status-badge ${student.externerSchueler ? 'status-info' : 'status-success'}">
                    ${student.externerSchueler ? '🔗 Extern' : '🏫 Intern'}
                </span>
            </td>
            <td>${student.zweiteFremdsprache}</td>
            <td>${student.musischesFach}</td>
            <td>${student.religioesesFach}</td>
            <td>${student.freiesFach}</td>
            <td>
                ${[student.freund1, student.freund2].filter(f => f).join(', ') || '-'}
            </td>
            <td>
                <span class="status-badge ${student.rechtzeitigAbgegeben ? 'status-success' : 'status-warning'}">
                    ${student.rechtzeitigAbgegeben ? '✓ Ja' : '✗ Nein'}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editStudent(${student.id})">Bearbeiten</button>
                <button class="btn btn-sm btn-danger" onclick="deleteStudent(${student.id})">Löschen</button>
            </td>
        </tr>
    `).join('');
    
    updateStudentCount(filteredStudents.length);
}

// Update student count
function updateStudentCount(count = students.length) {
    document.getElementById('studentCount').textContent = count;
}

// Edit student
function editStudent(id) {
    const student = findStudentById(id);
    if (!student) return;
    
    currentEditId = id;
    document.getElementById('nachname').value = student.nachname;
    document.getElementById('vorname').value = student.vorname;
    document.getElementById('geschlecht').value = student.geschlecht;
    document.getElementById('externerSchueler').checked = student.externerSchueler;
    document.getElementById('rechtzeitigAbgegeben').checked = student.rechtzeitigAbgegeben;
    document.getElementById('abgabedatum').value = student.abgabedatum || '';
    document.getElementById('zweiteFremdsprache').value = student.zweiteFremdsprache;
    document.getElementById('musischesFach').value = student.musischesFach;
    document.getElementById('religioesesFach').value = student.religioesesFach;
    document.getElementById('freiesFach').value = student.freiesFach;
    document.getElementById('freund1').value = student.freund1;
    document.getElementById('freund2').value = student.freund2;
    
    document.querySelector('.form-actions button[type="submit"]').textContent = 'Änderungen speichern';
    
    showTab('input');
}

// Delete student
function deleteStudent(id) {
    if (!confirm('Möchten Sie diesen Schüler wirklich löschen?')) return;
    
    deleteStudentFromServer(id);
}

// Find student by ID
function findStudentById(id) {
    return students.find(student => student.id === id);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Load students from server
async function loadStudentsFromServer() {
    try {
        const response = await fetch(`${API_BASE_URL}/students`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        students = data;
        renderStudentsTable();
        updateStudentCount();
        
    } catch (error) {
        console.error('Fehler beim Laden der Schüler:', error);
        showNotification('Fehler beim Laden der Schüler: ' + error.message, 'error');
    }
}

// Add student to server
async function addStudentToServer(student) {
    try {
        const response = await fetch(`${API_BASE_URL}/students`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(student)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const newStudent = await response.json();
        students.push(newStudent);
        renderStudentsTable();
        updateStudentCount();
        resetForm();
        showNotification('Schüler erfolgreich hinzugefügt!', 'success');
        
    } catch (error) {
        console.error('Fehler beim Hinzufügen des Schülers:', error);
        showNotification('Fehler beim Hinzufügen des Schülers: ' + error.message, 'error');
    }
}

// Update student on server
async function updateStudentOnServer(student) {
    try {
        const response = await fetch(`${API_BASE_URL}/students/${student.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(student)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const updatedStudent = await response.json();
        const index = students.findIndex(s => s.id === updatedStudent.id);
        if (index !== -1) {
            students[index] = updatedStudent;
        }
        
        renderStudentsTable();
        updateStudentCount();
        resetForm();
        showNotification('Schüler erfolgreich aktualisiert!', 'success');
        
    } catch (error) {
        console.error('Fehler beim Aktualisieren des Schülers:', error);
        showNotification('Fehler beim Aktualisieren des Schülers: ' + error.message, 'error');
    }
}

// Delete student from server
async function deleteStudentFromServer(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/students/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        students = students.filter(student => student.id !== id);
        renderStudentsTable();
        updateStudentCount();
        showNotification('Schüler erfolgreich gelöscht!', 'success');
        
    } catch (error) {
        console.error('Fehler beim Löschen des Schülers:', error);
        showNotification('Fehler beim Löschen des Schülers: ' + error.message, 'error');
    }
}

// Manual Class Editing Functions
let currentClassAssignments = null;
let hasUnsavedChanges = false;

// Load class assignments for editing
async function loadClassAssignments() {
    try {
        const response = await fetch(`${API_BASE_URL}/assignments`);
        
        if (!response.ok) {
            if (response.status === 404) {
                showNoAssignmentsMessage();
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        currentClassAssignments = data;
        hasUnsavedChanges = false;
        
        renderEditableClassAssignments(data);
        updateSaveButton();
        showNotification('Klassenzuordnungen geladen!', 'success');
        
    } catch (error) {
        console.error('Fehler beim Laden der Klassenzuordnungen:', error);
        showNotification('Fehler beim Laden der Klassenzuordnungen: ' + error.message, 'error');
        showNoAssignmentsMessage();
    }
}

// Show message when no assignments exist
function showNoAssignmentsMessage() {
    document.getElementById('classEditorContainer').style.display = 'none';
    document.getElementById('noAssignmentsMessage').style.display = 'block';
}

// Render editable class assignments
function renderEditableClassAssignments(data) {
    document.getElementById('noAssignmentsMessage').style.display = 'none';
    document.getElementById('classEditorContainer').style.display = 'block';
    
    // Update assignment info
    const timestamp = new Date(data.timestamp).toLocaleString('de-DE');
    document.getElementById('assignmentTimestamp').textContent = `Erstellt: ${timestamp}`;
    
    const manualEditIndicator = document.getElementById('manualEditIndicator');
    if (data.manuallyEdited) {
        manualEditIndicator.style.display = 'inline';
        const lastModified = new Date(data.lastModified).toLocaleString('de-DE');
        manualEditIndicator.title = `Zuletzt bearbeitet: ${lastModified}`;
    } else {
        manualEditIndicator.style.display = 'none';
    }
    
    // Render editable classes
    const container = document.getElementById('editableClassDisplay');
    container.innerHTML = data.assignments.map(classObj => `
        <div class="editable-class-card" data-class-id="${classObj.id}">
            <div class="editable-class-header">
                <h4>${classObj.name}</h4>
                <span class="class-size-badge">${classObj.students.length} Schüler</span>
            </div>
            <div class="editable-student-list" ondrop="dropStudent(event)" ondragover="allowDrop(event)">
                ${classObj.students.map(student => `
                    <div class="draggable-student" draggable="true" 
                         data-student-id="${student.id}" 
                         ondragstart="dragStudent(event)">
                        <div class="student-drag-info">
                            <div>
                                <div class="student-name">${student.vorname} ${student.nachname}</div>
                                <div class="student-details">
                                    ${student.geschlecht} | ${student.zweiteFremdsprache} | 
                                    Priorität: ${student.prioritaet || 0}
                                </div>
                            </div>
                            <div class="drag-handle">⋮⋮</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
    
    // Render statistics
    renderClassStatistics(data.assignments);
}

// Drag and drop functions
function dragStudent(event) {
    const studentId = event.target.closest('.draggable-student').dataset.studentId;
    const sourceClassId = event.target.closest('.editable-class-card').dataset.classId;
    
    event.dataTransfer.setData('text/plain', JSON.stringify({
        studentId: parseInt(studentId),
        sourceClassId: parseInt(sourceClassId)
    }));
    
    event.target.closest('.draggable-student').classList.add('dragging');
}

function allowDrop(event) {
    event.preventDefault();
    event.currentTarget.closest('.editable-class-card').classList.add('drag-over');
}

function dropStudent(event) {
    event.preventDefault();
    
    const targetClassCard = event.currentTarget.closest('.editable-class-card');
    targetClassCard.classList.remove('drag-over');
    
    try {
        const dragData = JSON.parse(event.dataTransfer.getData('text/plain'));
        const targetClassId = parseInt(targetClassCard.dataset.classId);
        
        // Don't move if dropping in the same class
        if (dragData.sourceClassId === targetClassId) {
            document.querySelector('.dragging')?.classList.remove('dragging');
            return;
        }
        
        moveStudentBetweenClasses(dragData.studentId, dragData.sourceClassId, targetClassId);
        
    } catch (error) {
        console.error('Error in drop:', error);
        showNotification('Fehler beim Verschieben des Schülers', 'error');
    }
    
    // Clean up drag state
    document.querySelector('.dragging')?.classList.remove('dragging');
}

// Move student between classes locally
function moveStudentBetweenClasses(studentId, sourceClassId, targetClassId) {
    if (!currentClassAssignments) return;
    
    // Find source and target classes
    const sourceClass = currentClassAssignments.assignments.find(c => c.id === sourceClassId);
    const targetClass = currentClassAssignments.assignments.find(c => c.id === targetClassId);
    
    if (!sourceClass || !targetClass) {
        showNotification('Fehler: Klasse nicht gefunden', 'error');
        return;
    }
    
    // Find and remove student from source class
    const studentIndex = sourceClass.students.findIndex(s => s.id === studentId);
    if (studentIndex === -1) {
        showNotification('Fehler: Schüler nicht gefunden', 'error');
        return;
    }
    
    const student = sourceClass.students.splice(studentIndex, 1)[0];
    
    // Add student to target class
    targetClass.students.push(student);
    
    // Update class statistics
    updateClassStats(sourceClass);
    updateClassStats(targetClass);
    
    // Mark as changed
    hasUnsavedChanges = true;
    updateSaveButton();
    
    // Re-render the display
    renderEditableClassAssignments(currentClassAssignments);
    
    showNotification(`${student.vorname} ${student.nachname} wurde zu ${targetClass.name} verschoben`, 'success');
}

// Update class statistics
function updateClassStats(classObj) {
    classObj.stats = {
        'männlich': 0,
        'weiblich': 0,
        'subjects': {}
    };
    
    classObj.students.forEach(student => {
        // Update gender count
        const gender = student.geschlecht;
        if (gender === 'männlich' || gender === 'weiblich') {
            classObj.stats[gender]++;
        }
        
        // Update subject count
        const subjects = [
            student.zweiteFremdsprache,
            student.musischesFach,
            student.religioesesFach,
            student.freiesFach
        ];
        
        subjects.forEach(subject => {
            if (subject && subject.trim()) {
                if (!classObj.stats.subjects[subject]) {
                    classObj.stats.subjects[subject] = 0;
                }
                classObj.stats.subjects[subject]++;
            }
        });
    });
}

// Render class statistics
function renderClassStatistics(classes) {
    const container = document.getElementById('classStatistics');
    
    container.innerHTML = classes.map(classObj => `
        <div class="stat-card">
            <h4>${classObj.name} (${classObj.students.length} Schüler)</h4>
            
            <div class="stat-row">
                <span class="stat-label">Männlich</span>
                <span class="stat-value">${classObj.stats?.männlich || 0}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Weiblich</span>
                <span class="stat-value">${classObj.stats?.weiblich || 0}</span>
            </div>
            
            ${Object.entries(classObj.stats?.subjects || {}).length > 0 ? `
                <h5 style="margin-top: 15px; margin-bottom: 10px; color: #666;">Fächer</h5>
                ${Object.entries(classObj.stats.subjects).map(([subject, count]) => `
                    <div class="stat-row">
                        <span class="stat-label">${subject}</span>
                        <span class="stat-value">${count}</span>
                    </div>
                `).join('')}
            ` : ''}
        </div>
    `).join('');
}

// Save class assignments
async function saveClassAssignments() {
    if (!currentClassAssignments || !hasUnsavedChanges) {
        showNotification('Keine Änderungen zum Speichern vorhanden', 'info');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/assignments`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentClassAssignments)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const updatedData = await response.json();
        currentClassAssignments = updatedData;
        hasUnsavedChanges = false;
        updateSaveButton();
        
        // Update the display with the saved data
        renderEditableClassAssignments(updatedData);
        
        showNotification('Klassenzuordnungen erfolgreich gespeichert!', 'success');
        
    } catch (error) {
        console.error('Fehler beim Speichern:', error);
        showNotification('Fehler beim Speichern: ' + error.message, 'error');
    }
}

// Reset class editor
function resetClassEditor() {
    if (hasUnsavedChanges) {
        if (!confirm('Sie haben ungespeicherte Änderungen. Möchten Sie wirklich zurücksetzen?')) {
            return;
        }
    }
    
    currentClassAssignments = null;
    hasUnsavedChanges = false;
    updateSaveButton();
    
    document.getElementById('classEditorContainer').style.display = 'none';
    document.getElementById('noAssignmentsMessage').style.display = 'block';
    
    showNotification('Editor wurde zurückgesetzt', 'info');
}

// Update save button state
function updateSaveButton() {
    const saveBtn = document.getElementById('saveClassesBtn');
    if (saveBtn) {
        saveBtn.disabled = !hasUnsavedChanges;
        saveBtn.textContent = hasUnsavedChanges ? 'Änderungen speichern *' : 'Änderungen speichern';
    }
}

// Enhance the existing DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    // ...existing code...
    
    // Prevent default dragover behavior on document
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    // Clean up drag states when drag ends
    document.addEventListener('dragend', function(e) {
        document.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
        document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    });
    
    // Warn about unsaved changes before leaving page
    window.addEventListener('beforeunload', function(e) {
        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = 'Sie haben ungespeicherte Änderungen. Möchten Sie die Seite wirklich verlassen?';
        }
    });
});

// Automatic class assignment function
async function assignClasses() {
    const numberOfClasses = parseInt(document.getElementById('numberOfClasses').value);
    
    if (!numberOfClasses || numberOfClasses < 1) {
        showNotification('Bitte geben Sie eine gültige Anzahl von Klassen ein.', 'error');
        return;
    }
    
    if (students.length === 0) {
        showNotification('Keine Schüler vorhanden. Bitte fügen Sie zuerst Schüler hinzu.', 'error');
        return;
    }
    
    try {
        showNotification('Klassenzuordnung wird erstellt...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/assignments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numberOfClasses: numberOfClasses
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display assignment results
        displayAssignmentResults(result);
        showNotification('Klassenzuordnung erfolgreich erstellt!', 'success');
        
    } catch (error) {
        console.error('Fehler bei der Klassenzuordnung:', error);
        showNotification('Fehler bei der Klassenzuordnung: ' + error.message, 'error');
    }
}

// Display assignment results
function displayAssignmentResults(data) {
    const resultsContainer = document.getElementById('assignmentResults');
    const classesDisplay = document.getElementById('classesDisplay');
    const conflictsDisplay = document.getElementById('conflictsDisplay');
    
    // Show results container
    resultsContainer.style.display = 'block';
    
    // Display classes
    if (data.assignments && data.assignments.length > 0) {
        classesDisplay.innerHTML = data.assignments.map(classObj => `
            <div class="class-result">
                <h5>Klasse ${classObj.id}</h5>
                <p><strong>Schüleranzahl:</strong> ${classObj.students.length}</p>
                <p><strong>Geschlechterverteilung:</strong> 
                   ${classObj.students.filter(s => s.geschlecht === 'männlich').length} männlich, 
                   ${classObj.students.filter(s => s.geschlecht === 'weiblich').length} weiblich</p>
                <div class="student-list">
                    ${classObj.students.map(student => 
                        `<span class="student-tag">${student.nachname}, ${student.vorname}</span>`
                    ).join('')}
                </div>
            </div>
        `).join('');
    }
    
    // Display conflicts if any
    if (data.conflicts && data.conflicts.length > 0) {
        conflictsDisplay.innerHTML = `
            <div class="conflicts-section">
                <h5>⚠️ Konflikte</h5>
                <ul>
                    ${data.conflicts.map(conflict => `<li>${conflict}</li>`).join('')}
                </ul>
            </div>
        `;
    } else {
        conflictsDisplay.innerHTML = '<div class="no-conflicts">✅ Keine Konflikte gefunden</div>';
    }
}

// Reset class assignments
async function resetClassAssignments() {
    // Prevent any default browser behavior
    try {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
    } catch (e) {
        // event might not be defined in some contexts
    }
    
    if (!confirm('Möchten Sie wirklich alle Klassenzuordnungen zurücksetzen?')) {
        return false;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/assignments`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            document.getElementById('assignmentResults').style.display = 'none';
            showNotification('Klassenzuordnungen zurückgesetzt!', 'success');
            
            // If we're on the classes tab, reload the assignments
            if (document.querySelector('.tab-btn.active').textContent.includes('Klassenzuordnung')) {            loadClassAssignments();
            }
        } else {
            throw new Error('Fehler beim Zurücksetzen der Zuordnungen');
        }
    } catch (error) {
        console.error('Fehler beim Zurücksetzen:', error);
        showNotification('Fehler beim Zurücksetzen: ' + error.message, 'error');
    }
    
    return false; // Explicitly prevent any form submission
}

// Export class assignments to JSON
function exportClassAssignments() {
    const assignmentResults = document.getElementById('assignmentResults');
    
    if (assignmentResults.style.display === 'none') {
        showNotification('Keine Klassenzuordnungen zum Exportieren vorhanden.', 'error');
        return;
    }
    
    // Get the current assignments from server
    fetch(`${API_BASE_URL}/assignments`)
        .then(response => response.json())
        .then(data => {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `klassenzuordnung_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showNotification('Klassenzuordnungen exportiert!', 'success');
        })
        .catch(error => {
            console.error('Fehler beim Exportieren:', error);
            showNotification('Fehler beim Exportieren: ' + error.message, 'error');
        });
}

// Print class assignments
function printClassAssignments() {
    const assignmentResults = document.getElementById('assignmentResults');
    
    if (assignmentResults.style.display === 'none') {
        showNotification('Keine Klassenzuordnungen zum Drucken vorhanden.', 'error');
        return;
    }
    
    const printWindow = window.open('', '_blank');
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Klassenzuordnungen - E-Phasen-Verteilung</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
                .class-result { margin-bottom: 30px; page-break-inside: avoid; }
                .class-result h5 { background: #f5f5f5; padding: 10px; margin: 0; border-left: 4px solid #007bff; }
                .student-list { margin-top: 10px; }
                .student-tag { display: inline-block; background: #e9ecef; padding: 4px 8px; margin: 2px; border-radius: 4px; font-size: 12px; }
                .conflicts-section { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin-top: 20px; }
                .no-conflicts { background: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin-top: 20px; }
                @media print { .no-print { display: none; } }
            </style>
        </head>
        <body>
            <h1>Klassenzuordnungen - E-Phasen-Verteilung</h1>
            <p><strong>Erstellt am:</strong> ${new Date().toLocaleDateString('de-DE')}</p>
            ${assignmentResults.innerHTML}
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.print();
}

// Export all student data to JSON
function exportData() {
    if (students.length === 0) {
        showNotification('Keine Daten zum Exportieren vorhanden.', 'error');
        return;
    }
    
    const exportData = {
        students: students,
        exportDate: new Date().toISOString(),
        totalStudents: students.length
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `schuelerdaten_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Daten erfolgreich exportiert!', 'success');
}

// Print student table
function printTable() {
    if (students.length === 0) {
        showNotification('Keine Daten zum Drucken vorhanden.', 'error');
        return;
    }
    
    const printWindow = window.open('', '_blank');
    const tableHTML = document.getElementById('studentsTable').outerHTML;
    
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Schülerliste - E-Phasen-Verteilung</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; font-size: 12px; }
                h1 { color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f8f9fa; font-weight: bold; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .actions { display: none; }
                @media print { 
                    .no-print, .actions { display: none; }
                    body { font-size: 10px; }
                    table { font-size: 10px; }
                }
            </style>
        </head>
        <body>
            <h1>Schülerliste - E-Phasen-Verteilung</h1>
            <p><strong>Anzahl Schüler:</strong> ${students.length}</p>
            <p><strong>Erstellt am:</strong> ${new Date().toLocaleDateString('de-DE')}</p>
            ${tableHTML.replace(/class="actions"/g, 'class="actions no-print"')}
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.print();
}