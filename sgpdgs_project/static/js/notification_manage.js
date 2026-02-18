// Notification Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Show/hide specific user field based on send_to selection
    const sendToSelect = document.querySelector('select[name="send_to"]');
    const specificUserField = document.getElementById('specificUserField');
    
    if (sendToSelect && specificUserField) {
        sendToSelect.addEventListener('change', function() {
            if (this.value === 'specific') {
                specificUserField.style.display = 'block';
            } else {
                specificUserField.style.display = 'none';
            }
        });
        
        // Trigger on page load
        if (sendToSelect.value === 'specific') {
            specificUserField.style.display = 'block';
        }
    }
});
