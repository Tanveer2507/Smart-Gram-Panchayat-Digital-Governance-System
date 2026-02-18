from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone
from .models import Notice
import datetime

def notice_list(request):
    notices = Notice.objects.filter(is_active=True, status='published')
    # Update statuses
    for notice in notices:
        notice.update_status()
    context = {'notices': notices}
    return render(request, 'notices/list.html', context)

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    # Increment view count
    notice.view_count += 1
    notice.save()
    return render(request, 'notices/detail.html', {'notice': notice})


@login_required
def admin_manage_notices(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Handle POST requests for add/edit/publish/delete
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            notice = Notice.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                category=request.POST.get('category'),
                target_audience=request.POST.get('target_audience', 'all'),
                is_urgent=request.POST.get('is_urgent') == 'on',
                created_by=request.user,
            )
            
            # Handle publish option
            publish_option = request.POST.get('publish_option')
            if publish_option == 'now':
                notice.status = 'published'
                notice.publish_date = timezone.now()
            elif publish_option == 'schedule':
                notice.status = 'scheduled'
                schedule_date = request.POST.get('schedule_date')
                schedule_time = request.POST.get('schedule_time')
                if schedule_date and schedule_time:
                    notice.publish_date = timezone.datetime.strptime(
                        f"{schedule_date} {schedule_time}", "%Y-%m-%d %H:%M"
                    )
            else:
                notice.status = 'draft'
            
            # Handle expiry date
            expiry_date = request.POST.get('expiry_date')
            if expiry_date:
                notice.expiry_date = timezone.datetime.strptime(expiry_date, "%Y-%m-%d")
            
            # Handle file upload
            if request.FILES.get('document'):
                notice.document = request.FILES['document']
            
            notice.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='New Notice Created',
                    message=f'Notice "{notice.title}" has been created by {request.user.username}.',
                    notification_type='notice',
                    related_link='/notices/admin/manage/'
                )
            
            messages.success(request, 'Notice created successfully!')
            return redirect('admin_manage_notices')
        
        elif action == 'edit':
            notice_id = request.POST.get('notice_id')
            notice = get_object_or_404(Notice, id=notice_id)
            notice.title = request.POST.get('title')
            notice.content = request.POST.get('content')
            notice.category = request.POST.get('category')
            notice.target_audience = request.POST.get('target_audience', 'all')
            notice.is_urgent = request.POST.get('is_urgent') == 'on'
            
            # Handle expiry date
            expiry_date = request.POST.get('expiry_date')
            if expiry_date:
                notice.expiry_date = timezone.datetime.strptime(expiry_date, "%Y-%m-%d")
            
            notice.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('admin_manage_notices')
        
        elif action == 'publish':
            notice_id = request.POST.get('notice_id')
            notice = get_object_or_404(Notice, id=notice_id)
            notice.status = 'published'
            notice.publish_date = timezone.now()
            notice.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='Notice Published',
                    message=f'Notice "{notice.title}" has been published by {request.user.username}.',
                    notification_type='notice',
                    related_link='/notices/admin/manage/'
                )
            
            messages.success(request, 'Notice published successfully!')
            return redirect('admin_manage_notices')
        
        elif action == 'unpublish':
            notice_id = request.POST.get('notice_id')
            notice = get_object_or_404(Notice, id=notice_id)
            notice.status = 'draft'
            notice.save()
            messages.success(request, 'Notice unpublished successfully!')
            return redirect('admin_manage_notices')
        
        elif action == 'schedule':
            notice_id = request.POST.get('notice_id')
            notice = get_object_or_404(Notice, id=notice_id)
            schedule_date = request.POST.get('schedule_date')
            schedule_time = request.POST.get('schedule_time')
            if schedule_date and schedule_time:
                notice.status = 'scheduled'
                notice.publish_date = timezone.datetime.strptime(
                    f"{schedule_date} {schedule_time}", "%Y-%m-%d %H:%M"
                )
                notice.save()
                messages.success(request, 'Notice scheduled successfully!')
            return redirect('admin_manage_notices')
        
        elif action == 'duplicate':
            notice_id = request.POST.get('notice_id')
            original = get_object_or_404(Notice, id=notice_id)
            notice = Notice.objects.create(
                title=f"{original.title} (Copy)",
                content=original.content,
                category=original.category,
                target_audience=original.target_audience,
                is_urgent=original.is_urgent,
                status='draft',
                created_by=request.user,
            )
            messages.success(request, 'Notice duplicated successfully!')
            return redirect('admin_manage_notices')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    audience_filter = request.GET.get('audience', '')
    
    # Get all notices
    notices = Notice.objects.all().select_related('created_by').order_by('-created_at')
    
    # Update statuses
    for notice in notices:
        notice.update_status()
    
    # Apply filters
    if search_query:
        notices = notices.filter(Q(title__icontains=search_query))
    
    if category_filter:
        notices = notices.filter(category=category_filter)
    
    if status_filter:
        notices = notices.filter(status=status_filter)
    
    if audience_filter:
        notices = notices.filter(target_audience=audience_filter)
    
    # Calculate statistics
    total_notices = Notice.objects.count()
    draft_notices = Notice.objects.filter(status='draft').count()
    published_notices = Notice.objects.filter(status='published').count()
    scheduled_notices = Notice.objects.filter(status='scheduled').count()
    expired_notices = Notice.objects.filter(status='expired').count()
    
    context = {
        'notices': notices,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'audience_filter': audience_filter,
        'total_notices': total_notices,
        'draft_notices': draft_notices,
        'published_notices': published_notices,
        'scheduled_notices': scheduled_notices,
        'expired_notices': expired_notices,
        'today': datetime.date.today().isoformat(),
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M'),
    }
    return render(request, 'notices/admin_manage_notices_professional.html', context)


@login_required
@require_http_methods(["GET"])
def notice_api_detail(request, pk):
    """API endpoint for fetching notice details"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    notice = get_object_or_404(Notice, pk=pk)
    
    data = {
        'id': notice.id,
        'title': notice.title,
        'content': notice.content,
        'category': notice.category,
        'category_display': notice.get_category_display(),
        'target_audience': notice.target_audience,
        'audience_display': notice.get_target_audience_display(),
        'status': notice.status,
        'status_display': notice.get_status_display(),
        'is_urgent': notice.is_urgent,
        'publish_date': notice.publish_date.strftime('%B %d, %Y %I:%M %p') if notice.publish_date else None,
        'expiry_date': notice.expiry_date.strftime('%B %d, %Y') if notice.expiry_date else None,
        'created_at': notice.created_at.strftime('%B %d, %Y'),
        'updated_at': notice.updated_at.strftime('%B %d, %Y'),
        'created_by': notice.created_by.username if notice.created_by else 'Unknown',
        'view_count': notice.view_count,
        'document_url': notice.document.url if notice.document else None,
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def notice_api_delete(request, pk):
    """API endpoint for deleting notices"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    notice = get_object_or_404(Notice, pk=pk)
    notice_title = notice.title
    
    # Create notification for admin
    from notifications.models import AdminNotification
    from django.contrib.auth.models import User
    
    # Get all admin users
    admin_users = User.objects.filter(is_staff=True, is_superuser=True)
    
    for admin in admin_users:
        AdminNotification.objects.create(
            user=admin,
            title='Notice Deleted',
            message=f'Notice "{notice_title}" has been deleted by {request.user.username}.',
            notification_type='notice',
            related_link='/notices/admin/manage/'
        )
    
    notice.delete()
    
    return JsonResponse({'success': True, 'message': 'Notice deleted successfully'})
