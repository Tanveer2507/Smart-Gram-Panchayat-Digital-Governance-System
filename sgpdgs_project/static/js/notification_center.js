// Notification Center JavaScript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function markAsRead(notificationId) {
    const markReadUrl = document.body.getAttribute('data-mark-read-url') || '/notifications/api/mark-read/';
    
    fetch(markReadUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            notification_id: notificationId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function markAsUnread(notificationId) {
    // Similar implementation for marking as unread
    alert('Mark as unread functionality - to be implemented');
}

function markAllAsRead() {
    if (confirm('Mark all notifications as read?')) {
        const markAllReadUrl = document.body.getAttribute('data-mark-all-read-url') || '/notifications/api/mark-all-read/';
        
        fetch(markAllReadUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    }
}
