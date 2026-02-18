from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Notification, UserNotification
from core.models import UserRole

@login_required
def admin_manage_notifications(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    from django.db.models import Q
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    priority_filter = request.GET.get('priority', '')
    
    # Get all notifications
    notifications = Notification.objects.all().select_related('created_by').order_by('-created_at')
    
    # Apply filters
    if search_query:
        notifications = notifications.filter(
            Q(title__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    if type_filter:
        notifications = notifications.filter(notification_type=type_filter)
    
    if priority_filter:
        notifications = notifications.filter(priority=priority_filter)
    
    # Status filter (active/inactive as sent/expired)
    if status_filter == 'sent':
        notifications = notifications.filter(is_active=True)
    elif status_filter == 'expired':
        notifications = notifications.filter(is_active=False)
    
    # Get statistics
    total_notifications = Notification.objects.count()
    active_notifications = Notification.objects.filter(is_active=True).count()
    draft_notifications = 0  # Can be implemented later
    scheduled_notifications = 0  # Can be implemented later
    expired_notifications = Notification.objects.filter(is_active=False).count()
    today = timezone.now().date()
    sent_today = Notification.objects.filter(created_at__date=today).count()
    
    context = {
        'notifications': notifications,
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'priority_filter': priority_filter,
        'total_notifications': total_notifications,
        'active_notifications': active_notifications,
        'draft_notifications': draft_notifications,
        'scheduled_notifications': scheduled_notifications,
        'expired_notifications': expired_notifications,
        'sent_today': sent_today,
    }
    return render(request, 'notifications/admin_manage.html', context)

@login_required
def admin_create_notification(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        priority = request.POST.get('priority')
        target_all = request.POST.get('target_all') == 'on'
        target_roles = request.POST.get('target_roles', '')
        expires_at = request.POST.get('expires_at')
        
        # Create notification
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            created_by=request.user,
            target_all_users=target_all,
            target_roles=target_roles,
            expires_at=expires_at if expires_at else None
        )
        
        # Create user notifications
        if target_all:
            users = User.objects.filter(is_active=True)
        else:
            # Filter by roles
            role_list = [r.strip() for r in target_roles.split(',') if r.strip()]
            users = User.objects.filter(role__role__in=role_list, is_active=True)
        
        for user in users:
            UserNotification.objects.create(
                notification=notification,
                user=user
            )
        
        messages.success(request, f'Notification created and sent to {users.count()} users!')
        return redirect('admin_manage_notifications')
    
    # Get all roles for the form
    roles = UserRole.ROLE_CHOICES
    
    context = {
        'roles': roles,
    }
    return render(request, 'notifications/admin_create.html', context)

@login_required
def admin_edit_notification(request, notification_id):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.method == 'POST':
        notification.title = request.POST.get('title')
        notification.message = request.POST.get('message')
        notification.notification_type = request.POST.get('notification_type')
        notification.priority = request.POST.get('priority')
        notification.is_active = request.POST.get('is_active') == 'on'
        notification.save()
        
        messages.success(request, 'Notification updated successfully!')
        return redirect('admin_manage_notifications')
    
    context = {
        'notification': notification,
    }
    return render(request, 'notifications/admin_edit.html', context)

@login_required
def admin_delete_notification(request, notification_id):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    notification = get_object_or_404(Notification, id=notification_id)
    title = notification.title
    notification.delete()
    
    messages.success(request, f'Notification "{title}" deleted successfully!')
    return redirect('admin_manage_notifications')

@login_required
def user_notifications(request):
    # Get user notifications
    user_notifications = UserNotification.objects.filter(
        user=request.user,
        notification__is_active=True
    ).select_related('notification')
    
    # Mark as read if requested
    if request.GET.get('mark_read'):
        notif_id = request.GET.get('mark_read')
        try:
            user_notif = UserNotification.objects.get(id=notif_id, user=request.user)
            user_notif.is_read = True
            user_notif.read_at = timezone.now()
            user_notif.save()
        except UserNotification.DoesNotExist:
            pass
    
    # Get unread count
    unread_count = user_notifications.filter(is_read=False).count()
    
    context = {
        'user_notifications': user_notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/user_list.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@login_required
@require_http_methods(["GET"])
def get_admin_notifications(request):
    """API endpoint to get admin notifications for dropdown"""
    from .models import AdminNotification
    
    # Get recent UNREAD notifications only (last 10)
    notifications = AdminNotification.objects.filter(
        user=request.user,
        is_read=False  # Only unread notifications
    ).order_by('-created_at')[:10]
    
    unread_count = AdminNotification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    notifications_data = []
    for notif in notifications:
        notifications_data.append({
            'id': notif.id,
            'title': notif.title,
            'message': notif.message[:100] + '...' if len(notif.message) > 100 else notif.message,
            'type': notif.notification_type,
            'related_link': notif.related_link,
            'is_read': notif.is_read,
            'created_at': notif.created_at.strftime('%b %d, %Y %I:%M %p'),
            'time_ago': get_time_ago(notif.created_at),
        })
    
    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count,
    })

@login_required
@require_http_methods(["POST"])
def mark_notification_read(request):
    """API endpoint to mark notification as read"""
    from .models import AdminNotification
    
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        notification = AdminNotification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        unread_count = AdminNotification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return JsonResponse({
            'success': True,
            'unread_count': unread_count,
        })
    except AdminNotification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Notification not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """API endpoint to mark all notifications as read"""
    from .models import AdminNotification
    
    AdminNotification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    return JsonResponse({
        'success': True,
        'unread_count': 0,
    })

@login_required
def admin_notification_center(request):
    """Full notification management page for admin"""
    from .models import AdminNotification
    
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    
    notifications = AdminNotification.objects.filter(user=request.user)
    
    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)
    elif filter_type == 'read':
        notifications = notifications.filter(is_read=True)
    
    # Get statistics
    total_count = AdminNotification.objects.filter(user=request.user).count()
    unread_count = AdminNotification.objects.filter(user=request.user, is_read=False).count()
    read_count = AdminNotification.objects.filter(user=request.user, is_read=True).count()
    
    context = {
        'notifications': notifications,
        'filter_type': filter_type,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
    }
    return render(request, 'notifications/admin_notification_center.html', context)

@login_required
@require_http_methods(["POST"])
def delete_admin_notification(request, notification_id):
    """Delete a specific admin notification"""
    from .models import AdminNotification
    
    try:
        notification = AdminNotification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.delete()
        
        messages.success(request, 'Notification deleted successfully!')
        return redirect('admin_notification_center')
    except AdminNotification.DoesNotExist:
        messages.error(request, 'Notification not found!')
        return redirect('admin_notification_center')

def get_time_ago(dt):
    """Helper function to get human-readable time difference"""
    from django.utils.timesince import timesince
    return timesince(dt).split(',')[0] + ' ago'
