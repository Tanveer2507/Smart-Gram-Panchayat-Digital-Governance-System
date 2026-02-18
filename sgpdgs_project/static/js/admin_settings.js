// Admin Settings JavaScript

// Dark Mode Management
const darkModeToggle = document.getElementById('darkModeToggle');
const enableRegistrationToggle = document.getElementById('enableRegistrationToggle');
const approvalRequiredToggle = document.getElementById('approvalRequiredToggle');

// Load saved dark mode preference
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    if (darkModeToggle) darkModeToggle.checked = true;
}

// Dark mode toggle
if (darkModeToggle) {
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
        }
    });
}

// Tab switching
function showTab(tabName) {
    // Hide all sections
    const sections = document.querySelectorAll('.settings-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.settings-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected section
    const selectedSection = document.getElementById(tabName + '-section');
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    // Add active class to clicked tab
    event.target.closest('.settings-tab').classList.add('active');
}

// Save settings functions
function saveGeneralSettings(event) {
    event.preventDefault();
    alert('General settings saved successfully!');
}

function saveAllSettings(event) {
    event.preventDefault();
    alert('All settings saved successfully!');
}
