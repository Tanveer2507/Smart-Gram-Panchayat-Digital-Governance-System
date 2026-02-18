// Notification System JavaScript
(function() {
    'use strict';
    
    // State management
    const NotificationSystem = {
        panelOpen: false,
        refreshInterval: null,
        isLoading: false,
        currentUnreadCount: null,
        lastUpdateTime: 0,
        
        getCookie: function(name) {
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
        },
        
        updateBadge: function(count) {
            // Get stored count from localStorage
            const storedCount = localStorage.getItem('notificationUnreadCount');
            const storedCountNum = storedCount ? parseInt(storedCount) : null;
            
            // Only update if count has actually changed
            if (storedCountNum === count && this.currentUnreadCount === count) {
                return;
            }
            
            this.currentUnreadCount = count;
            localStorage.setItem('notificationUnreadCount', count.toString());
            
            const badge = document.getElementById('notificationBadge');
            
            if (badge) {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
            }
        },
        
        loadNotifications: function(forceLoad = false) {
            // Prevent multiple simultaneous requests
            if (this.isLoading) {
                return;
            }
            
            // Throttle requests - don't load more than once per 2 seconds unless forced
            const now = Date.now();
            if (!forceLoad && (now - this.lastUpdateTime) < 2000) {
                return;
            }
            
            this.isLoading = true;
            this.lastUpdateTime = now;
            
            // Get the URL from a data attribute or use a default
            const notificationUrl = document.body.getAttribute('data-notification-url') || '/notifications/api/get/';
            
            fetch(notificationUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.updateBadge(data.unread_count);
                        
                        // Only render if panel is open
                        if (this.panelOpen) {
                            this.renderNotifications(data.notifications);
                        }
                    }
                })
                .catch(error => console.error('Error loading notifications:', error))
                .finally(() => {
                    this.isLoading = false;
                });
        },
        
        renderNotifications: function(notifications) {
            const listContainer = document.getElementById('notificationList');
            if (!listContainer) return;
            
            if (notifications.length === 0) {
                listContainer.innerHTML = `
                    <div class="notification-empty">
                        <i class="fas fa-bell-slash"></i>
                        <p>No new notifications</p>
                    </div>
                `;
                return;
            }
            
            let html = '';
            notifications.forEach(notif => {
                // Only show unread notifications (backend already filters, but double check)
                if (!notif.is_read) {
                    const safeLink = notif.related_link || '';
                    
                    html += `
                        <div class="notification-item unread" id="notif-${notif.id}" onclick="NotificationSystem.handleClick(${notif.id}, '${safeLink}')">
                            <div class="notification-item-header">
                                <div class="notification-item-title">
                                    <i class="fas fa-circle" style="font-size: 0.5rem; color: var(--primary-light); margin-right: 0.5rem;"></i>
                                    ${notif.title}
                                </div>
                                <div class="notification-item-time">${notif.time_ago}</div>
                            </div>
                            <div class="notification-item-message">${notif.message}</div>
                        </div>
                    `;
                }
            });
            
            if (html === '') {
                listContainer.innerHTML = `
                    <div class="notification-empty">
                        <i class="fas fa-bell-slash"></i>
                        <p>No new notifications</p>
                    </div>
                `;
            } else {
                listContainer.innerHTML = html;
            }
        },
        
        removeNotificationFromUI: function(notificationId) {
            const notifElement = document.getElementById('notif-' + notificationId);
            if (notifElement) {
                // Add fade out animation
                notifElement.style.transition = 'all 0.3s ease';
                notifElement.style.opacity = '0';
                notifElement.style.transform = 'translateX(20px)';
                
                // Remove after animation
                setTimeout(() => {
                    notifElement.remove();
                    
                    // Check if list is empty
                    const listContainer = document.getElementById('notificationList');
                    if (listContainer && listContainer.children.length === 0) {
                        listContainer.innerHTML = `
                            <div class="notification-empty">
                                <i class="fas fa-bell-slash"></i>
                                <p>No new notifications</p>
                            </div>
                        `;
                    }
                }, 300);
            }
        },
        
        clearAllNotificationsFromUI: function() {
            const listContainer = document.getElementById('notificationList');
            if (listContainer) {
                // Fade out all notifications
                const notifItems = listContainer.querySelectorAll('.notification-item');
                notifItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.transition = 'all 0.3s ease';
                        item.style.opacity = '0';
                        item.style.transform = 'translateX(20px)';
                    }, index * 50); // Stagger animation
                });
                
                // Clear and show empty state after animation
                setTimeout(() => {
                    listContainer.innerHTML = `
                        <div class="notification-empty">
                            <i class="fas fa-bell-slash"></i>
                            <p>No new notifications</p>
                        </div>
                    `;
                }, notifItems.length * 50 + 300);
            }
        },
        
        handleClick: function(notificationId, relatedLink) {
            // First remove from UI with animation
            this.removeNotificationFromUI(notificationId);
            
            // Get the URL from a data attribute or use a default
            const markReadUrl = document.body.getAttribute('data-mark-read-url') || '/notifications/api/mark-read/';
            
            // Then mark as read in backend
            fetch(markReadUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    notification_id: notificationId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.updateBadge(data.unread_count);
                    
                    // Redirect if there's a link (after a small delay for animation)
                    if (relatedLink && relatedLink !== 'None' && relatedLink !== '') {
                        setTimeout(() => {
                            window.location.href = relatedLink;
                        }, 300);
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        },
        
        markAllAsRead: function() {
            // First clear UI with animation
            this.clearAllNotificationsFromUI();
            
            // Update badge immediately
            this.updateBadge(0);
            
            // Get the URL from a data attribute or use a default
            const markAllReadUrl = document.body.getAttribute('data-mark-all-read-url') || '/notifications/api/mark-all-read/';
            
            // Then mark as read in backend
            fetch(markAllReadUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.updateBadge(0);
                }
            })
            .catch(error => console.error('Error:', error));
        },
        
        togglePanel: function() {
            const panel = document.getElementById('notificationSlidePanel');
            if (!panel) return;
            
            this.panelOpen = !this.panelOpen;
            
            if (this.panelOpen) {
                panel.classList.add('show');
                document.body.style.overflow = 'hidden';
                this.loadNotifications(true); // Force load when opening panel
            } else {
                panel.classList.remove('show');
                document.body.style.overflow = '';
            }
        },
        
        closePanel: function() {
            const panel = document.getElementById('notificationSlidePanel');
            if (panel) {
                panel.classList.remove('show');
                document.body.style.overflow = '';
                this.panelOpen = false;
            }
        },
        
        init: function() {
            // Load stored count immediately from localStorage
            const storedCount = localStorage.getItem('notificationUnreadCount');
            if (storedCount !== null) {
                const count = parseInt(storedCount);
                const badge = document.getElementById('notificationBadge');
                if (badge) {
                    badge.textContent = count;
                    badge.style.display = count > 0 ? 'flex' : 'none';
                }
                this.currentUnreadCount = count;
            }
            
            // Bell icon click handler
            const notificationBell = document.getElementById('notificationBell');
            if (notificationBell) {
                notificationBell.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.togglePanel();
                });
            }
            
            // Overlay click handler
            const overlay = document.getElementById('notificationOverlay');
            if (overlay) {
                overlay.addEventListener('click', () => {
                    this.closePanel();
                });
            }
            
            // Load notifications in background (throttled)
            setTimeout(() => {
                this.loadNotifications();
            }, 500);
            
            // Set up refresh interval
            if (!this.refreshInterval) {
                this.refreshInterval = setInterval(() => {
                    this.loadNotifications();
                }, 30000); // 30 seconds
            }
        }
    };
    
    // Expose to global scope for onclick handlers
    window.NotificationSystem = NotificationSystem;
    window.markAllAsRead = function() {
        NotificationSystem.markAllAsRead();
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            NotificationSystem.init();
        });
    } else {
        // DOM already loaded
        NotificationSystem.init();
    }
})();
