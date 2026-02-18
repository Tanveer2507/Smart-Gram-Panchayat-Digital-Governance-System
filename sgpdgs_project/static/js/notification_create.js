// Notification Create Form JavaScript
function toggleRoles() {
    const targetAll = document.getElementById('targetAll');
    const rolesSection = document.getElementById('rolesSection');
    rolesSection.style.display = targetAll.checked ? 'none' : 'block';
}
