from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint

def complaint_list(request):
    complaints = Complaint.objects.all()
    if request.user.is_authenticated:
        user_complaints = complaints.filter(user=request.user)
    else:
        user_complaints = []
    
    context = {
        'complaints': complaints[:10],
        'user_complaints': user_complaints,
    }
    return render(request, 'complaints/list.html', context)

@login_required
def complaint_create(request):
    if request.method == 'POST':
        complaint = Complaint.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            priority=request.POST.get('priority', 'medium'),
            location=request.POST.get('location', ''),
        )
        if request.FILES.get('image'):
            complaint.image = request.FILES['image']
            complaint.save()
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('complaint_list')
    return render(request, 'complaints/create.html')

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/complaint_detail_view.html', {'complaint': complaint})


@login_required
def admin_manage_complaints(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    from django.db.models import Q
    from django.contrib.auth.models import User
    
    # Handle POST requests for add/edit/status/assign/remark
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'edit':
            complaint_id = request.POST.get('complaint_id')
            complaint = get_object_or_404(Complaint, id=complaint_id)
            complaint.title = request.POST.get('title')
            complaint.description = request.POST.get('description')
            complaint.category = request.POST.get('category')
            complaint.priority = request.POST.get('priority')
            complaint.save()
            messages.success(request, 'Complaint updated successfully!')
            return redirect('admin_manage_complaints')
        
        elif action == 'status':
            complaint_id = request.POST.get('complaint_id')
            complaint = get_object_or_404(Complaint, id=complaint_id)
            old_status = complaint.status
            new_status = request.POST.get('status')
            complaint.status = new_status
            admin_remarks = request.POST.get('admin_remarks', '')
            if admin_remarks:
                complaint.admin_remarks = admin_remarks
            complaint.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            status_display = dict(Complaint._meta.get_field('status').choices).get(new_status, new_status)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='Complaint Status Updated',
                    message=f'Complaint "{complaint.title}" status changed to {status_display} by {request.user.username}.',
                    notification_type='complaint',
                    related_link='/complaints/admin/manage/'
                )
            
            messages.success(request, 'Complaint status updated successfully!')
            return redirect('admin_manage_complaints')
        
        elif action == 'assign':
            complaint_id = request.POST.get('complaint_id')
            assigned_to_id = request.POST.get('assigned_to')
            complaint = get_object_or_404(Complaint, id=complaint_id)
            if assigned_to_id:
                complaint.assigned_to = User.objects.get(id=assigned_to_id)
                complaint.save()
                messages.success(request, 'Staff assigned successfully!')
            return redirect('admin_manage_complaints')
        
        elif action == 'remark':
            complaint_id = request.POST.get('complaint_id')
            complaint = get_object_or_404(Complaint, id=complaint_id)
            complaint.admin_remarks = request.POST.get('admin_remarks', '')
            complaint.save()
            messages.success(request, 'Remark added successfully!')
            return redirect('admin_manage_complaints')
        
        else:
            # Add new complaint
            complaint = Complaint.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                priority=request.POST.get('priority', 'medium'),
            )
            if request.FILES.get('attachment'):
                complaint.image = request.FILES['attachment']
                complaint.save()
            messages.success(request, 'Complaint created successfully!')
            return redirect('admin_manage_complaints')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    
    # Get all complaints
    complaints = Complaint.objects.all().select_related('user', 'assigned_to').order_by('-created_at')
    
    # Apply filters
    if search_query:
        complaints = complaints.filter(
            Q(id__icontains=search_query) |
            Q(title__icontains=search_query)
        )
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    
    if category_filter:
        complaints = complaints.filter(category__icontains=category_filter)
    
    # Calculate statistics
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='submitted').count()
    in_progress_complaints = Complaint.objects.filter(status='in_progress').count()
    resolved_complaints = Complaint.objects.filter(status='resolved').count()
    rejected_complaints = Complaint.objects.filter(status='rejected').count()
    
    # Get staff users for assignment
    staff_users = User.objects.filter(is_staff=True)
    
    context = {
        'complaints': complaints,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
        'rejected_complaints': rejected_complaints,
        'staff_users': staff_users,
    }
    return render(request, 'complaints/admin_manage_complaints_professional.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@login_required
@require_http_methods(["GET"])
def complaint_api_detail(request, pk):
    """API endpoint for fetching complaint details"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    complaint = get_object_or_404(Complaint, pk=pk)
    
    data = {
        'id': complaint.id,
        'title': complaint.title,
        'description': complaint.description,
        'category': complaint.category,
        'priority': complaint.priority,
        'status': complaint.status,
        'created_at': complaint.created_at.strftime('%B %d, %Y'),
        'updated_at': complaint.updated_at.strftime('%B %d, %Y'),
        'user_name': complaint.user.get_full_name() or complaint.user.username,
        'user_email': complaint.user.email or 'No email',
        'user_phone': getattr(complaint.user, 'phone', None),
        'assigned_to': complaint.assigned_to.username if complaint.assigned_to else None,
        'admin_remarks': complaint.admin_remarks or '',
        'location': complaint.location or '',
        'image_url': complaint.image.url if complaint.image else None,
    }
    
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def complaint_api_delete(request, pk):
    """API endpoint for deleting complaints"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    complaint = get_object_or_404(Complaint, pk=pk)
    complaint.delete()
    
    return JsonResponse({'success': True, 'message': 'Complaint deleted successfully'})
