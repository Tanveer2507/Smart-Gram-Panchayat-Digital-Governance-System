// Base Template JavaScript
// Auto-hide toasts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
    });
    
    // Show all toasts
    toastList.forEach(function(toast) {
        toast.show();
    });
});
