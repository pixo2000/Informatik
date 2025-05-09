// API endpoints
const API = {
    getAllEntries: 'http://localhost:8000/api/atlas/entries',
    getEntryById: (id) => `http://localhost:8000/api/atlas/entry/${id}`,
    createEntry: 'http://localhost:8000/api/atlas/entry',
    updateEntry: (id) => `http://localhost:8000/api/atlas/entry/${id}`,
    deleteEntry: (id) => `http://localhost:8000/api/atlas/entry/${id}`
};

// DOM elements
const entriesContainer = document.getElementById('entries-container');
const entryView = document.querySelector('.entry-view');
const entriesList = document.querySelector('.entries-list');
const entryTitle = document.getElementById('entry-title');
const entryDate = document.getElementById('entry-date');
const entryAuthor = document.getElementById('entry-author');
const entryContent = document.getElementById('entry-content');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const statsElement = document.getElementById('stats');

// Auth elements
const authModal = document.getElementById('auth-modal');
const atlasKeyInput = document.getElementById('atlas-key');
const authSubmitButton = document.getElementById('auth-submit');
const authErrorMessage = document.getElementById('auth-error');
const logoutLink = document.getElementById('logout-link');

// Form elements
const uploadSection = document.getElementById('upload-section');
const entryForm = document.getElementById('entry-form');
const formTitle = document.getElementById('entry-form-title');
const formAuthor = document.getElementById('entry-form-author');
const formContent = document.getElementById('entry-form-content');
const formMessage = document.getElementById('form-message');
const saveEntryButton = document.getElementById('save-entry');
const cancelEntryButton = document.getElementById('cancel-entry');

// Edit elements
const editSection = document.getElementById('edit-section');
const editForm = document.getElementById('edit-form');
const editFormId = document.getElementById('edit-form-id');
const editFormTitle = document.getElementById('edit-form-title');
const editFormAuthor = document.getElementById('edit-form-author');
const editFormContent = document.getElementById('edit-form-content');
const editFormMessage = document.getElementById('edit-form-message');
const updateEntryButton = document.getElementById('update-entry');
const cancelEditButton = document.getElementById('cancel-edit');

// Entry actions
const editEntryButton = document.getElementById('edit-entry');
const deleteEntryButton = document.getElementById('delete-entry');
const backButton = document.getElementById('back-button');

// Global variables
let currentEntryId = null;
let atlasKey = null;

// Check for stored key with expiration
const checkStoredKey = () => {
    const storedData = localStorage.getItem('atlasKeyData');
    if (!storedData) return null;
    
    try {
        const keyData = JSON.parse(storedData);
        const now = Date.now();
        
        // Check if the key has expired (10 minutes = 600000 milliseconds)
        if (now > keyData.expiresAt) {
            console.log('Stored key has expired - clearing');
            localStorage.removeItem('atlasKeyData');
            return null;
        }
        
        console.log(`Key valid for ${Math.round((keyData.expiresAt - now) / 60000)} more minutes`);
        return keyData.key;
    } catch (e) {
        console.error('Error parsing stored key data:', e);
        localStorage.removeItem('atlasKeyData');
        return null;
    }
};

// Initialize stored key
const storedKey = checkStoredKey();
if (storedKey) {
    console.log('Found valid stored key - will validate on page load');
    atlasKey = storedKey;
}

// Auth functions
function checkAuthentication() {
    console.log('Checking authentication...');
    console.log('Stored Atlas Key in localStorage:', !!atlasKey);
    
    if (!atlasKey) {
        showAuthModal();
    } else {
        console.log('Using stored key from localStorage');
        // Verify the key works by making a test API call
        fetchEntries();
    }
}

function showAuthModal() {
    // Clear the input field before showing the modal
    atlasKeyInput.value = '';
    authErrorMessage.textContent = '';
    authModal.style.display = 'flex';
}

function hideAuthModal() {
    authModal.style.display = 'none';
}

function handleAuthentication() {
    const key = atlasKeyInput.value.trim();
    
    if (!key) {
        authErrorMessage.textContent = 'Please enter a valid key';
        return;
    }
    
    // Store the key temporarily
    atlasKey = key;
    
    console.log('Attempting authentication...');
    console.log('API Endpoint:', API.getAllEntries);
    
    // Test the key by fetching entries
    fetch(API.getAllEntries, {
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(response => {
        console.log('Authentication response status:', response.status);
        console.log('Authentication response headers:', Object.fromEntries([...response.headers.entries()]));
        
        if (!response.ok) {
            throw new Error(`Authentication failed with status: ${response.status}`);
        }
        return response.json().catch(err => {
            console.error('Error parsing JSON:', err);
            throw new Error('Invalid JSON in response');
        });
    })
    .then(data => {
        console.log('Authentication successful, data received:', data);
        
        // Store key with 10-minute expiration
        const expiresAt = Date.now() + 600000; // Current time + 10 minutes
        const keyData = { key: atlasKey, expiresAt };
        localStorage.setItem('atlasKeyData', JSON.stringify(keyData));
        
        console.log(`Key will expire at: ${new Date(expiresAt).toLocaleTimeString()}`);
        
        hideAuthModal();
        displayEntries(data.entries); // Changed from data to data.entries
    })
    .catch(error => {
        console.error('Authentication error details:', error);
        atlasKey = null;
        authErrorMessage.textContent = `Error: ${error.message}. Check console for details.`;
    });
}

function logout() {
    localStorage.removeItem('atlasKeyData');
    atlasKey = null;
    // Clear the input field when logging out
    atlasKeyInput.value = '';
    authErrorMessage.textContent = '';
    showAuthModal();
}

// API functions with auth headers
function fetchEntries() {
    entriesContainer.innerHTML = '<div class="entry-loading">Loading data...</div>'; 
    
    fetch(API.getAllEntries, {
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(handleResponse)
    .then(data => {
        displayEntries(data.entries); // Changed from data to data.entries
    })
    .catch(handleError);
}

function fetchEntry(id) {
    fetch(API.getEntryById(id), {
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(handleResponse)
    .then(data => {
        displayEntryDetails(data);
    })
    .catch(handleError);
}

function createNewEntry(entryData) {
    fetch(API.createEntry, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        },
        body: JSON.stringify(entryData)
    })
    .then(handleResponse)
    .then(data => {
        formMessage.textContent = 'Entry created successfully';
        formMessage.className = 'success';
        resetForm();
        setTimeout(() => {
            hideUploadForm();
            fetchEntries();
        }, 1500);
    })
    .catch(error => {
        formMessage.textContent = `Error: ${error.message}`;
        formMessage.className = 'error';
    });
}

function updateExistingEntry(id, entryData) {
    fetch(API.updateEntry(id), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        },
        body: JSON.stringify(entryData)
    })
    .then(handleResponse)
    .then(data => {
        editFormMessage.textContent = 'Entry updated successfully';
        editFormMessage.className = 'success';
        setTimeout(() => {
            hideEditForm();
            fetchEntry(id);
        }, 1500);
    })
    .catch(error => {
        editFormMessage.textContent = `Error: ${error.message}`;
        editFormMessage.className = 'error';
    });
}

function deleteEntry(id) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }
    
    fetch(API.deleteEntry(id), {
        method: 'DELETE',
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(handleResponse)
    .then(() => {
        backToEntryList();
        fetchEntries();
    })
    .catch(handleError);
}

// Helper functions
function handleResponse(response) {
    console.log(`API Response [${response.url}]:`, {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries([...response.headers.entries()])
    });
    
    if (response.status === 401) {
        // Authentication failed
        console.error('Authentication failed (401 Unauthorized)');
        logout();
        throw new Error('Authentication failed. Please login again.');
    }
    
    if (!response.ok) {
        console.error(`API error: ${response.status} - ${response.statusText}`);
        throw new Error(`API error: ${response.status} - ${response.statusText}`);
    }
    
    return response.json().catch(err => {
        console.error('Error parsing JSON:', err);
        throw new Error('Failed to parse server response as JSON');
    });
}

function handleError(error) {
    console.error('API Error:', error);
    entriesContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
}

// Display functions to match the API structure
function displayEntries(entries) {
    entriesContainer.innerHTML = '';
    
    if (!entries || entries.length === 0) {
        entriesContainer.innerHTML = '<div class="entry-loading">No entries found</div>';
        return;
    }
    
    entries.forEach(entry => {
        const entryCard = document.createElement('div');
        entryCard.className = 'entry-card';
        entryCard.dataset.id = entry.id;
        
        entryCard.innerHTML = `
            <h3>${entry.name || 'No Name'}</h3>
            <div class="entry-meta">
                <span>Contact: ${entry.phone || 'N/A'}</span> | 
                <span>${entry.email || 'No email'}</span>
            </div>
            <p>${entry.notes ? entry.notes.substring(0, 100) + '...' : 'No notes available'}</p>
        `;
        
        entryCard.addEventListener('click', () => viewEntry(entry.id));
        entriesContainer.appendChild(entryCard);
    });
    
    // Update stats
    statsElement.textContent = `${entries.length} entries in database`;
}

function displayEntryDetails(entry) {
    if (!entry) return;
    
    currentEntryId = entry.id;
    entriesList.classList.add('hidden');
    entryView.classList.remove('hidden');
    
    entryTitle.textContent = entry.name || 'No Name';
    entryDate.textContent = entry.phone || 'N/A';
    entryAuthor.textContent = entry.email || 'No email';
    
    // Format the address if it exists
    let addressText = '';
    if (entry.address) {
        const addr = entry.address;
        addressText = [
            addr.street,
            addr.city,
            addr.state,
            addr.postal_code,
            addr.country
        ].filter(Boolean).join(', ');
    }
    
    // Display address and notes
    entryContent.innerHTML = `
        <strong>Address:</strong><br>
        ${addressText || 'No address provided'}<br><br>
        <strong>Notes:</strong><br>
        ${entry.notes || 'No notes available'}
    `;
}

function viewEntry(id) {
    currentEntryId = id;
    fetchEntry(id);
}

function backToEntryList() {
    entryView.classList.add('hidden');
    entriesList.classList.remove('hidden');
    currentEntryId = null;
}

// Form handling
function showUploadForm() {
    entriesList.classList.add('hidden');
    entryView.classList.add('hidden');
    uploadSection.classList.remove('hidden');
}

function hideUploadForm() {
    uploadSection.classList.add('hidden');
    entriesList.classList.remove('hidden');
    resetForm();
}

function resetForm() {
    entryForm.reset();
    formMessage.textContent = '';
    formMessage.className = '';
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const entryData = {
        name: formTitle.value.trim(),
        email: formAuthor.value.trim(),
        notes: formContent.value.trim(),
        phone: null,
        address: null
    };
    
    createNewEntry(entryData);
}

// Edit functions
function showEditForm() {
    if (!currentEntryId) return;
    
    // Get the current entry data
    fetch(API.getEntryById(currentEntryId), {
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(handleResponse)
    .then(entry => {
        editFormId.value = entry.id;
        editFormTitle.value = entry.name;
        editFormAuthor.value = entry.email || '';
        editFormContent.value = entry.notes;
        
        entryView.classList.add('hidden');
        editSection.classList.remove('hidden');
    })
    .catch(handleError);
}

function hideEditForm() {
    editSection.classList.add('hidden');
    editForm.reset();
    editFormMessage.textContent = '';
    editFormMessage.className = '';
}

function handleEditFormSubmit(e) {
    e.preventDefault();
    
    const id = editFormId.value;
    const entryData = {
        name: editFormTitle.value.trim(),
        email: editFormAuthor.value.trim(),
        notes: editFormContent.value.trim()
    };
    
    updateExistingEntry(id, entryData);
}

// Search function
function searchEntries() {
    const query = searchInput.value.trim().toLowerCase();
    
    if (!query) {
        fetchEntries();
        return;
    }
    
    // Client-side search implementation to match our data structure
    fetch(API.getAllEntries, {
        headers: {
            'ATLAS-KEY': atlasKey  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(handleResponse)
    .then(data => {
        const allEntries = data.entries; // Extract entries array
        const filteredEntries = allEntries.filter(entry => 
            (entry.name && entry.name.toLowerCase().includes(query)) || 
            (entry.email && entry.email.toLowerCase().includes(query)) ||
            (entry.notes && entry.notes.toLowerCase().includes(query)) ||
            (entry.phone && entry.phone.toLowerCase().includes(query)) ||
            (entry.address && entry.address.city && entry.address.city.toLowerCase().includes(query))
        );
        
        displayEntries(filteredEntries);
    })
    .catch(handleError);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the UI based on auth state BEFORE checking authentication
    if (atlasKey) {
        // We already have a key, make sure modal stays hidden
        hideAuthModal();
        console.log('Using stored key - modal will remain hidden');
    } else {
        // No key, we'll show the auth modal
        console.log('No stored key found - will display login form');
    }
    
    // Now run the normal authentication check
    checkAuthentication();
    
    // Auth events
    authSubmitButton.addEventListener('click', handleAuthentication);
    atlasKeyInput.addEventListener('keyup', e => {
        if (e.key === 'Enter') handleAuthentication();
    });
    logoutLink.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });
    
    // Navigation events
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            if (link.textContent === 'Upload') {
                showUploadForm();
            } else if (link.textContent === 'Home') {
                hideUploadForm();
                backToEntryList();
                fetchEntries();
            }
            // Add more navigation handling as needed
        });
    });
    
    // Search events
    searchButton.addEventListener('click', searchEntries);
    searchInput.addEventListener('keyup', e => {
        if (e.key === 'Enter') searchEntries();
    });
    
    // Form events
    entryForm.addEventListener('submit', handleFormSubmit);
    cancelEntryButton.addEventListener('click', hideUploadForm);
    
    // Edit events
    editForm.addEventListener('submit', handleEditFormSubmit);
    cancelEditButton.addEventListener('click', () => {
        hideEditForm();
        entryView.classList.remove('hidden');
    });
    
    // Entry action events
    backButton.addEventListener('click', backToEntryList);
    editEntryButton.addEventListener('click', showEditForm);
    deleteEntryButton.addEventListener('click', () => deleteEntry(currentEntryId));
    
    // Keyboard shortcuts
    document.addEventListener('keyup', e => {
        if (e.key === 'Escape') {
            if (!entryView.classList.contains('hidden')) {
                backToEntryList();
            } else if (!uploadSection.classList.contains('hidden')) {
                hideUploadForm();
            } else if (!editSection.classList.contains('hidden')) {
                hideEditForm();
                entryView.classList.remove('hidden');
            }
        }
    });
});

// Debug utility
function debugAPI() {
    console.log('Current API configuration:');
    console.log('API Endpoints:', API);
    console.log('Atlas Key defined:', !!atlasKey);
    console.log('Current Entry ID:', currentEntryId);
    
    // Test the API endpoints
    fetch(API.getAllEntries, {
        headers: {
            'ATLAS-KEY': atlasKey || 'no-key-provided'  // Changed from ATLAS_KEY to ATLAS-KEY
        }
    })
    .then(response => {
        console.log('Test API call response:', {
            url: response.url,
            status: response.status,
            statusText: response.statusText,
            headers: Object.fromEntries([...response.headers.entries()])
        });
        return response.text(); // Get raw text instead of JSON
    })
    .then(text => {
        console.log('Raw API response:', text);
        try {
            const json = JSON.parse(text);
            console.log('Parsed JSON:', json);
        } catch (e) {
            console.log('Response is not valid JSON');
        }
    })
    .catch(error => {
        console.error('API test error:', error);
    });
}

// Force re-authentication by clearing the stored key
function forceAuthentication() {
    console.log('Forcing re-authentication...');
    localStorage.removeItem('atlasKeyData');
    atlasKey = null;
    // Clear the input field when forcing re-authentication
    atlasKeyInput.value = '';
    authErrorMessage.textContent = '';
    showAuthModal();
}

// Add developer tools to window object for console access
window.atlasDebug = {
    checkAPI: debugAPI,
    showKey: () => console.log('Current key:', atlasKey),
    forceLogin: forceAuthentication,
    clearStorage: () => {
        localStorage.removeItem('atlasKeyData');
        console.log('Atlas key removed from localStorage');
    },
    testEndpoints: () => {
        Object.entries(API).forEach(([name, endpoint]) => {
            if (typeof endpoint === 'string') {
                console.log(`Testing ${name}:`, endpoint);
            } else {
                console.log(`${name} is a function, testing with ID '123':`);
                console.log(endpoint('123'));
            }
        });
    },
    getKeyExpiration: () => {
        const storedData = localStorage.getItem('atlasKeyData');
        if (!storedData) {
            console.log('No key stored');
            return;
        }
        
        try {
            const keyData = JSON.parse(storedData);
            const now = Date.now();
            const minutesLeft = Math.round((keyData.expiresAt - now) / 60000);
            
            console.log(`Key expires at: ${new Date(keyData.expiresAt).toLocaleTimeString()}`);
            console.log(`Minutes remaining: ${minutesLeft}`);
        } catch (e) {
            console.error('Error parsing stored key data:', e);
        }
    }
};

// Add key event listener for debug console
document.addEventListener('keydown', e => {
    // Ctrl+Shift+D to open debug console
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        console.log('%c ATLAS API DEBUGGER ', 'background: #32CD32; color: black; font-size: 16px;');
        console.log('Type these commands to debug:');
        console.log('atlasDebug.checkAPI() - Test the API connection');
        console.log('atlasDebug.showKey() - Show the current API key');
        console.log('atlasDebug.forceLogin() - Force re-authentication');
        console.log('atlasDebug.clearStorage() - Clear the stored API key');
        console.log('atlasDebug.testEndpoints() - Test all API endpoints');
    }
});
