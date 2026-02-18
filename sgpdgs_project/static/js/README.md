# JavaScript Files Organization

Yeh folder mein sabhi JavaScript files ko organize kiya gaya hai. Har file ka apna specific purpose hai.

## Files aur unka Usage:

### 1. **base.js**
- **Usage**: `base.html` template mein
- **Purpose**: Toast notifications ko auto-hide karna
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/base.js' %}"></script>
  ```

### 2. **notification_system.js**
- **Usage**: Sabhi admin pages mein jahan notification dropdown hai
- **Purpose**: Real-time notification system, badge updates, panel management
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/notification_system.js' %}"></script>
  ```
- **Required HTML elements**:
  - `notificationBell` - Bell icon
  - `notificationBadge` - Unread count badge
  - `notificationSlidePanel` - Notification panel
  - `notificationList` - Notifications list container

### 3. **notification_center.js**
- **Usage**: `admin_notification_center.html` mein
- **Purpose**: Notification center page ke functions (mark as read, delete, etc.)
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/notification_center.js' %}"></script>
  ```

### 4. **notification_manage.js**
- **Usage**: `admin_manage.html` (notifications) mein
- **Purpose**: Notification management form ke functions
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/notification_manage.js' %}"></script>
  ```

### 5. **notification_create.js**
- **Usage**: `admin_create.html` (notifications) mein
- **Purpose**: Notification create form ke functions (role toggle)
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/notification_create.js' %}"></script>
  ```

### 6. **admin_sidebar.js**
- **Usage**: Sabhi admin professional templates mein
- **Purpose**: Mobile sidebar toggle functionality
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/admin_sidebar.js' %}"></script>
  ```

### 7. **admin_settings.js**
- **Usage**: `admin_settings_professional.html` mein
- **Purpose**: Settings page ke functions (dark mode, tab switching, save settings)
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/admin_settings.js' %}"></script>
  ```

### 8. **admin_manage_users.js**
- **Usage**: `admin_manage_users.html` mein
- **Purpose**: User management page ke functions (tooltips initialization)
- **Include kaise karein**:
  ```html
  <script src="{% static 'js/admin_manage_users.js' %}"></script>
  ```

### 9. **budget_dashboard.js**
- **Usage**: `budget/dashboard.html` mein
- **Purpose**: Budget dashboard charts (Chart.js integration)
- **Include kaise karein**:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="{% static 'js/budget_dashboard.js' %}"></script>
  ```
- **Note**: Chart.js library pehle load honi chahiye

## Template Updates Required:

Har template mein inline `<script>` tags ko replace karna hoga external JS files se:

### Example - base.html:
```html
<!-- Old -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Toast code...
    });
</script>

<!-- New -->
<script src="{% static 'js/base.js' %}"></script>
```

### Example - Admin Templates:
```html
<!-- Old -->
<script>
    function toggleSidebar() {
        // Sidebar code...
    }
</script>

<!-- New -->
<script src="{% static 'js/admin_sidebar.js' %}"></script>
```

## Benefits:

1. **Code Reusability**: Ek hi code multiple pages mein use ho sakta hai
2. **Maintainability**: Ek jagah change karo, sab jagah update ho jayega
3. **Performance**: Browser caching se faster loading
4. **Organization**: Clean aur organized code structure
5. **Debugging**: Aasani se debug kar sakte hain

## Next Steps:

1. Har HTML template mein inline `<script>` tags ko remove karein
2. Appropriate external JS files ko include karein
3. Test karein ki sab kuch properly work kar raha hai
4. Browser console mein errors check karein

## Notes:

- Sabhi files ES5/ES6 compatible hain
- Bootstrap 5 aur Font Awesome dependencies required hain
- CSRF token handling included hai
- LocalStorage use kiya gaya hai notification count ke liye
