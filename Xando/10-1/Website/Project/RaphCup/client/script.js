const API_BASE = 'http://localhost:5000/api';

// Global variables
let currentEmail = '';

// Utility functions
function showError(message) {
    alert('Fehler: ' + message);
}

function showSuccess(message) {
    alert('Erfolg: ' + message);
}

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(API_BASE + endpoint, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Ein Fehler ist aufgetreten');
        }
        
        return result;
    } catch (error) {
        throw error;
    }
}

// Authentication functions
async function register(email, password) {
    return await apiCall('/register', 'POST', { email, password });
}

async function login(email, password) {
    return await apiCall('/login', 'POST', { email, password });
}

async function verifyEmail(email, code) {
    return await apiCall('/verify', 'POST', { email, code });
}

async function resendVerification(email) {
    return await apiCall('/resend-verification', 'POST', { email });
}

async function forgotPassword(email) {
    return await apiCall('/forgot-password', 'POST', { email });
}

async function logout() {
    return await apiCall('/logout', 'POST');
}

// Tournament functions
async function getTournaments() {
    return await apiCall('/tournaments');
}

async function createTournament(tournamentData) {
    return await apiCall('/tournaments', 'POST', tournamentData);
}

async function registerForTournament(registrationData) {
    return await apiCall('/register_tournament', 'POST', registrationData);
}

async function getUserTournaments() {
    return await apiCall('/user/tournaments');
}

async function getTournamentRegistrations(tournamentId) {
    return await apiCall(`/admin/registrations/${tournamentId}`);
}

async function getUserProfile() {
    return await apiCall('/user/profile');
}

// Page-specific initialization
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    
    if (path.includes('index.html') || path === '/') {
        initHomePage();
    } else if (path.includes('login.html')) {
        initLoginPage();
    } else if (path.includes('register.html')) {
        initRegisterPage();
    } else if (path.includes('dashboard.html')) {
        initDashboardPage();
    } else if (path.includes('admin.html')) {
        initAdminPage();
    }
});

// Home page initialization
function initHomePage() {
    loadTournaments();
}

async function loadTournaments() {
    try {
        const tournaments = await getTournaments();
        const tournamentList = document.getElementById('tournament-list');
        
        if (!tournamentList) return;
        
        if (tournaments.length === 0) {
            tournamentList.innerHTML = '<p class="text-center">Keine Turniere verfügbar</p>';
            return;
        }
        
        tournamentList.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3>${tournament.name}</h3>
                <div class="tournament-info">
                    <p><strong>Beschreibung:</strong> ${tournament.description}</p>
                    <p><strong>Datum Option 1:</strong> ${new Date(tournament.date1).toLocaleString('de-DE')}</p>
                    <p><strong>Datum Option 2:</strong> ${new Date(tournament.date2).toLocaleString('de-DE')}</p>
                    <p><strong>Anmeldeschluss:</strong> ${new Date(tournament.registration_deadline).toLocaleString('de-DE')}</p>
                    <p><strong>Max. Spieler:</strong> ${tournament.max_players}</p>
                </div>
                <a href="login.html" class="btn btn-primary">Anmelden</a>
            </div>
        `).join('');
    } catch (error) {
        console.error('Fehler beim Laden der Turniere:', error);
    }
}

// Login page initialization
function initLoginPage() {
    const loginForm = document.getElementById('loginForm');
    const verifyForm = document.getElementById('verifyForm');
    const resetForm = document.getElementById('resetForm');
    const forgotPasswordBtn = document.getElementById('forgotPassword');
    const backToLoginBtn = document.getElementById('backToLogin');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (verifyForm) {
        verifyForm.addEventListener('submit', handleVerification);
    }
    
    if (resetForm) {
        resetForm.addEventListener('submit', handlePasswordReset);
    }
    
    if (forgotPasswordBtn) {
        forgotPasswordBtn.addEventListener('click', showPasswordReset);
    }
    
    if (backToLoginBtn) {
        backToLoginBtn.addEventListener('click', showLoginForm);
    }
}

function showPasswordReset(e) {
    e.preventDefault();
    document.getElementById('resetSection').style.display = 'block';
    document.getElementById('verificationSection').style.display = 'none';
    document.getElementById('backToLogin').style.display = 'inline';
    document.getElementById('forgotPassword').style.display = 'none';
}

function showLoginForm(e) {
    e.preventDefault();
    document.getElementById('resetSection').style.display = 'none';
    document.getElementById('verificationSection').style.display = 'none';
    document.getElementById('backToLogin').style.display = 'none';
    document.getElementById('forgotPassword').style.display = 'inline';
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        currentEmail = email;
        const result = await login(email, password);
        showSuccess(result.message);
        
        if (result.is_admin) {
            window.location.href = 'admin.html';
        } else {
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        if (error.message.includes('verify')) {
            document.getElementById('verificationSection').style.display = 'block';
            showError('Bitte verifizieren Sie zuerst Ihre E-Mail.');
        } else {
            showError(error.message);
        }
    }
}

async function handleVerification(e) {
    e.preventDefault();
    
    const code = document.getElementById('verificationCode').value;
    
    try {
        const result = await verifyEmail(currentEmail, code);
        showSuccess(result.message);
        document.getElementById('verificationSection').style.display = 'none';
        // Try to login again after verification
        const loginResult = await login(currentEmail, document.getElementById('password').value);
        if (loginResult.is_admin) {
            window.location.href = 'admin.html';
        } else {
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        showError(error.message);
    }
}

async function handlePasswordReset(e) {
    e.preventDefault();
    
    const email = document.getElementById('resetEmail').value;
    
    try {
        const result = await forgotPassword(email);
        showSuccess(result.message);
        document.getElementById('resetForm').reset();
        showLoginForm(e);
    } catch (error) {
        showError(error.message);
    }
}

// Register page initialization
function initRegisterPage() {
    const registerForm = document.getElementById('registerForm');
    const verifyForm = document.getElementById('verifyForm');
    const resendCodeBtn = document.getElementById('resendCode');
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    if (verifyForm) {
        verifyForm.addEventListener('submit', handleEmailVerification);
    }
    
    if (resendCodeBtn) {
        resendCodeBtn.addEventListener('click', handleResendCode);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showError('Passwörter stimmen nicht überein');
        return;
    }
    
    if (password.length < 6) {
        showError('Passwort muss mindestens 6 Zeichen lang sein');
        return;
    }
    
    try {
        currentEmail = email;
        const result = await register(email, password);
        showSuccess(result.message);
        
        // Show verification section
        document.getElementById('registerSection').style.display = 'none';
        document.getElementById('verificationSection').style.display = 'block';
    } catch (error) {
        showError(error.message);
    }
}

async function handleEmailVerification(e) {
    e.preventDefault();
    
    const code = document.getElementById('verificationCode').value;
    
    try {
        const result = await verifyEmail(currentEmail, code);
        showSuccess(result.message);
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
    } catch (error) {
        showError(error.message);
    }
}

async function handleResendCode(e) {
    e.preventDefault();
    
    try {
        const result = await resendVerification(currentEmail);
        showSuccess(result.message);
    } catch (error) {
        showError(error.message);
    }
}

// Dashboard page initialization
function initDashboardPage() {
    loadDashboardTournaments();
    loadUserTournaments();
    setupRegistrationModal();
    setupLogout();
    checkAdminStatus();
}

async function loadDashboardTournaments() {
    try {
        const tournaments = await getTournaments();
        const tournamentList = document.getElementById('tournamentList');
        
        if (!tournamentList) return;
        
        if (tournaments.length === 0) {
            tournamentList.innerHTML = '<p class="text-center">Keine Turniere verfügbar</p>';
            return;
        }
        
        tournamentList.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3>${tournament.name}</h3>
                <div class="tournament-info">
                    <p><strong>Beschreibung:</strong> ${tournament.description}</p>
                    <p><strong>Datum Option 1:</strong> ${new Date(tournament.date1).toLocaleString('de-DE')}</p>
                    <p><strong>Datum Option 2:</strong> ${new Date(tournament.date2).toLocaleString('de-DE')}</p>
                    <p><strong>Anmeldeschluss:</strong> ${new Date(tournament.registration_deadline).toLocaleString('de-DE')}</p>
                    <p><strong>Max. Spieler:</strong> ${tournament.max_players}</p>
                </div>
                <button class="btn btn-primary" onclick="openRegistrationModal(${tournament.id}, '${tournament.date1}', '${tournament.date2}')">
                    Anmelden
                </button>
            </div>
        `).join('');
    } catch (error) {
        showError('Fehler beim Laden der Turniere: ' + error.message);
    }
}

async function loadUserTournaments() {
    try {
        const tournaments = await getUserTournaments();
        const myTournaments = document.getElementById('myTournaments');
        
        if (!myTournaments) return;
        
        if (tournaments.length === 0) {
            myTournaments.innerHTML = '<p class="text-center">Sie sind für keine Turniere angemeldet</p>';
            return;
        }
        
        myTournaments.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3>${tournament.name}</h3>
                <div class="tournament-info">
                    <p><strong>Status:</strong> ${tournament.status}</p>
                    <p><strong>Ihre Datums-Abstimmung:</strong> ${new Date(tournament.date_vote).toLocaleString('de-DE')}</p>
                    <p><strong>Angemeldet am:</strong> ${new Date(tournament.registered_at).toLocaleString('de-DE')}</p>
                </div>
                <span class="btn btn-secondary">Bereits angemeldet</span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Fehler beim Laden der eigenen Turniere:', error);
    }
}

function setupRegistrationModal() {
    const modal = document.getElementById('registrationModal');
    const closeBtn = document.querySelector('.close');
    const form = document.getElementById('tournamentRegForm');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
    
    if (form) {
        form.addEventListener('submit', handleTournamentRegistration);
    }
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function openRegistrationModal(tournamentId, date1, date2) {
    const modal = document.getElementById('registrationModal');
    const tournamentIdInput = document.getElementById('tournamentId');
    const dateVoteSelect = document.getElementById('dateVote');
    
    tournamentIdInput.value = tournamentId;
    
    dateVoteSelect.innerHTML = `
        <option value="">Datum auswählen</option>
        <option value="${date1}">${new Date(date1).toLocaleString('de-DE')}</option>
        <option value="${date2}">${new Date(date2).toLocaleString('de-DE')}</option>
    `;
    
    modal.style.display = 'block';
}

async function handleTournamentRegistration(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const registrationData = {
        tournament_id: formData.get('tournamentId'),
        discord_tag: formData.get('discordTag'),
        valorant_rank: formData.get('valorantRank'),
        valorant_peak: formData.get('valorantPeak'),
        date_vote: formData.get('dateVote')
    };
    
    try {
        const result = await registerForTournament(registrationData);
        showSuccess(result.message);
        document.getElementById('registrationModal').style.display = 'none';
        e.target.reset();
        // Reload tournaments to update UI
        loadDashboardTournaments();
        loadUserTournaments();
    } catch (error) {
        showError(error.message);
    }
}

async function checkAdminStatus() {
    try {
        const profile = await getUserProfile();
        if (profile.is_admin) {
            const adminLinks = document.querySelectorAll('.admin-only');
            adminLinks.forEach(link => link.style.display = 'inline');
        }
    } catch (error) {
        console.error('Fehler beim Laden des Profils:', error);
    }
}

// Admin page initialization
function initAdminPage() {
    const createTournamentForm = document.getElementById('createTournamentForm');
    
    if (createTournamentForm) {
        createTournamentForm.addEventListener('submit', handleCreateTournament);
    }
    
    loadAdminTournaments();
    setupLogout();
}

async function loadAdminTournaments() {
    try {
        const tournaments = await getTournaments();
        const adminTournamentList = document.getElementById('adminTournamentList');
        
        if (!adminTournamentList) return;
        
        if (tournaments.length === 0) {
            adminTournamentList.innerHTML = '<p class="text-center">Keine Turniere vorhanden</p>';
            return;
        }
        
        adminTournamentList.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3>${tournament.name}</h3>
                <div class="tournament-info">
                    <p><strong>Beschreibung:</strong> ${tournament.description}</p>
                    <p><strong>Status:</strong> ${tournament.status}</p>
                    <p><strong>Max. Spieler:</strong> ${tournament.max_players}</p>
                    <p><strong>Erstellt am:</strong> ${new Date(tournament.created_at).toLocaleString('de-DE')}</p>
                </div>
                <button class="btn btn-primary" onclick="loadRegistrations(${tournament.id})">
                    Anmeldungen anzeigen
                </button>
            </div>
        `).join('');
    } catch (error) {
        showError('Fehler beim Laden der Turniere: ' + error.message);
    }
}

async function loadRegistrations(tournamentId) {
    try {
        const registrations = await getTournamentRegistrations(tournamentId);
        const registrationsList = document.getElementById('registrationsList');
        
        if (!registrationsList) return;
        
        if (registrations.length === 0) {
            registrationsList.innerHTML = '<p class="text-center">Keine Anmeldungen für dieses Turnier</p>';
            return;
        }
        
        const registrationsHtml = `
            <h3>Anmeldungen für Turnier ${tournamentId}</h3>
            <div class="registrations-table">
                <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
                    <thead>
                        <tr style="background-color: var(--card-bg); border-bottom: 2px solid var(--primary-color);">
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">E-Mail</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">Discord</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">Aktueller Rang</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">Peak Rang</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">Datums-Vote</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid var(--border-color);">Anmeldedatum</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${registrations.map(reg => `
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${reg.email}</td>
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${reg.discord_tag || 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${reg.valorant_rank || 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${reg.valorant_peak || 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${new Date(reg.date_vote).toLocaleString('de-DE')}</td>
                                <td style="padding: 8px; border: 1px solid var(--border-color);">${new Date(reg.registered_at).toLocaleString('de-DE')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        registrationsList.innerHTML = registrationsHtml;
    } catch (error) {
        showError('Fehler beim Laden der Anmeldungen: ' + error.message);
    }
}

async function handleCreateTournament(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const tournamentData = {
        name: formData.get('name'),
        description: formData.get('description'),
        date1: formData.get('date1'),
        date2: formData.get('date2'),
        registration_deadline: formData.get('registrationDeadline'),
        max_players: parseInt(formData.get('maxPlayers'))
    };
    
    // Validate dates
    const now = new Date();
    const date1 = new Date(tournamentData.date1);
    const date2 = new Date(tournamentData.date2);
    const deadline = new Date(tournamentData.registration_deadline);
    
    if (deadline >= date1 || deadline >= date2) {
        showError('Anmeldeschluss muss vor beiden Turnier-Daten liegen');
        return;
    }
    
    if (date1 <= now || date2 <= now) {
        showError('Turnier-Daten müssen in der Zukunft liegen');
        return;
    }
    
    try {
        const result = await createTournament(tournamentData);
        showSuccess(result.message);
        e.target.reset();
        loadAdminTournaments();
    } catch (error) {
        showError(error.message);
    }
}

// Common functions
function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                await logout();
                window.location.href = 'index.html';
            } catch (error) {
                showError('Fehler beim Ausloggen: ' + error.message);
            }
        });
    }
}
