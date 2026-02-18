"""
Script to create sample admin notifications for testing
Run with: python sgpdgs_project/manage.py shell < sgpdgs_project/create_sample_notifications.py
"""

from django.contrib.auth.models import User
from notifications.models import AdminNotification
from django.utils import timezone

# Get admin user
admin_user = User.objects.filter(is_superuser=True).first()

if admin_user:
    # Create sample notifications
    notifications_data = [
        {
            'title': 'New Complaint Submitted',
            'message': 'A new complaint has been submitted by John Doe regarding water supply issue.',
            'notification_type': 'complaint',
            'related_link': '/complaints/admin/manage/',
        },
        {
            'title': 'Certificate Request Pending',
            'message': 'Certificate request for Income Certificate from Jane Smith is awaiting approval.',
            'notification_type': 'certificate',
            'related_link': '/certificates/admin/manage/',
        },
        {
            'title': 'New User Registration',
            'message': 'A new user "citizen123" has registered and is awaiting account activation.',
            'notification_type': 'user',
            'related_link': '/manage-users/',
        },
        {
            'title': 'Budget Alert',
            'message': 'Infrastructure Development budget has exceeded 80% utilization.',
            'notification_type': 'budget',
            'related_link': '/budget/admin/manage/',
        },
        {
            'title': 'New Notice Published',
            'message': 'Notice regarding "Village Meeting Schedule" has been published successfully.',
            'notification_type': 'notice',
            'related_link': '/notices/admin/manage/',
        },
        {
            'title': 'System Maintenance',
            'message': 'Scheduled system maintenance will occur on Sunday at 2:00 AM.',
            'notification_type': 'system',
            'related_link': '',
        },
    ]
    
    for notif_data in notifications_data:
        AdminNotification.objects.create(
            user=admin_user,
            **notif_data
        )
    
    print(f"✓ Created {len(notifications_data)} sample notifications for {admin_user.username}")
    print(f"✓ Unread count: {AdminNotification.objects.filter(user=admin_user, is_read=False).count()}")
else:
    print("✗ No admin user found. Please create an admin user first.")
