from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from complaints.models import Complaint
from certificates.models import Certificate
from budget.models import BudgetRecord
from notices.models import Notice
from .models import UserRole

def home(request):
    stats = {
        'total_complaints': Complaint.objects.count(),
        'pending_certificates': Certificate.objects.filter(status='pending').count(),
        'total_budget': BudgetRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'active_notices': Notice.objects.filter(is_active=True).count(),
    }
    
    recent_notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'stats': stats,
        'recent_notices': recent_notices,
    }
    return render(request, 'core/home.html', context)

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        village = request.POST.get('village')
        address = request.POST.get('address')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = full_name.split()[0] if full_name else ''
        user.last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
        user.save()
        
        # Create user role
        UserRole.objects.create(
            user=user,
            role='citizen',
            phone=phone,
            village=village,
            address=address
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'core/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Check if user is admin/staff and redirect accordingly
            if user.is_staff and user.is_superuser:
                messages.success(request, f'Welcome Administrator {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def dashboard(request):
    # Redirect admins to admin dashboard
    if request.user.is_staff and request.user.is_superuser:
        return redirect('admin_dashboard')
    
    user_role = getattr(request.user, 'role', None)
    
    # Get user-specific data
    user_complaints = Complaint.objects.filter(user=request.user)
    user_certificates = Certificate.objects.filter(user=request.user)
    
    context = {
        'user_role': user_role,
        'user_complaints': user_complaints,
        'user_certificates': user_certificates,
        'total_complaints': user_complaints.count(),
        'total_certificates': user_certificates.count(),
        'pending_complaints': user_complaints.filter(status='submitted').count(),
        'pending_certificates': user_certificates.filter(status='pending').count(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def profile(request):
    user_role = getattr(request.user, 'role', None)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        if user_role:
            user_role.phone = request.POST.get('phone')
            user_role.village = request.POST.get('village')
            user_role.address = request.POST.get('address')
            user_role.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    user_complaints = Complaint.objects.filter(user=request.user)
    user_certificates = Certificate.objects.filter(user=request.user)
    
    context = {
        'user_role': user_role,
        'total_complaints': user_complaints.count(),
        'total_certificates': user_certificates.count(),
        'pending_items': user_complaints.filter(status='submitted').count() + user_certificates.filter(status='pending').count(),
    }
    return render(request, 'core/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect!')
            return redirect('change_password')
        
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match!')
            return redirect('change_password')
        
        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, 'Password changed successfully! Please login again.')
        return redirect('login')
    
    return render(request, 'core/change_password.html')

# Role-specific login views
def sarpanch_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'role') and user.role.role == 'sarpanch':
            login(request, user)
            messages.success(request, f'Welcome Sarpanch {user.get_full_name()}!')
            return redirect('sarpanch_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized as Sarpanch!')
    return render(request, 'core/role_login.html', {'role': 'Sarpanch', 'icon': 'user-tie'})

@login_required
def sarpanch_dashboard(request):
    # Check if user is sarpanch
    if not hasattr(request.user, 'role') or request.user.role.role != 'sarpanch':
        messages.error(request, 'Access denied! Sarpanch privileges required.')
        return redirect('home')
    
    # Get all statistics
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='submitted').count()
    total_certificates = Certificate.objects.count()
    pending_certificates = Certificate.objects.filter(status='pending').count()
    total_budget = BudgetRecord.objects.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    active_notices = Notice.objects.filter(is_active=True).count()
    
    # Recent activities
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
    recent_certificates = Certificate.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'total_certificates': total_certificates,
        'pending_certificates': pending_certificates,
        'total_budget': total_budget,
        'active_notices': active_notices,
        'recent_complaints': recent_complaints,
        'recent_certificates': recent_certificates,
    }
    return render(request, 'core/sarpanch_dashboard.html', context)

def secretary_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'role') and user.role.role == 'panchayat_secretary':
            login(request, user)
            messages.success(request, f'Welcome Secretary {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized as Secretary!')
    return render(request, 'core/role_login.html', {'role': 'Panchayat Secretary', 'icon': 'user-cog'})

def accountant_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'role') and user.role.role == 'accountant':
            login(request, user)
            messages.success(request, f'Welcome Accountant {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized as Accountant!')
    return render(request, 'core/role_login.html', {'role': 'Accountant', 'icon': 'calculator'})

def block_officer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'role') and user.role.role == 'block_officer':
            login(request, user)
            messages.success(request, f'Welcome Block Officer {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized as Block Officer!')
    return render(request, 'core/role_login.html', {'role': 'Block Officer', 'icon': 'user-check'})

# Admin login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff and user.is_superuser:
            login(request, user)
            messages.success(request, f'Welcome Administrator {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials or not authorized!')
    return render(request, 'core/admin_login.html')

@login_required
def admin_dashboard(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Get all statistics
    total_users = User.objects.count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='submitted').count()
    total_certificates = Certificate.objects.count()
    pending_certificates = Certificate.objects.filter(status='pending').count()
    total_budget = BudgetRecord.objects.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    total_spent = BudgetRecord.objects.aggregate(Sum('spent_amount'))['spent_amount__sum'] or 0
    active_notices = Notice.objects.filter(is_active=True).count()
    
    # Recent activities
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
    recent_certificates = Certificate.objects.all().order_by('-created_at')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    # Role distribution
    from django.db.models import Count
    role_distribution = UserRole.objects.values('role').annotate(count=Count('role'))
    
    context = {
        'total_users': total_users,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'total_certificates': total_certificates,
        'pending_certificates': pending_certificates,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': total_budget - total_spent,
        'active_notices': active_notices,
        'recent_complaints': recent_complaints,
        'recent_certificates': recent_certificates,
        'recent_users': recent_users,
        'role_distribution': role_distribution,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def admin_manage_users(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    from django.utils import timezone
    from django.db.models import Q, Count
    from datetime import timedelta
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    # Get all users
    users = User.objects.all().select_related('role').order_by('-date_joined')
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply role filter
    if role_filter:
        users = users.filter(role__role=role_filter)
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Calculate statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    today = timezone.now().date()
    new_today = User.objects.filter(date_joined__date=today).count()
    admin_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    
    # Calculate teacher and student counts (if roles exist)
    teacher_users = UserRole.objects.filter(role='panchayat_secretary').count()
    student_users = UserRole.objects.filter(role='citizen').count()
    
    # Get role distribution with display names
    role_distribution = UserRole.objects.values('role').annotate(count=Count('role'))
    
    # Add display names to role distribution
    role_stats = []
    for role_data in role_distribution:
        role_code = role_data['role']
        role_display = dict(UserRole.ROLE_CHOICES).get(role_code, role_code)
        role_stats.append({
            'role': role_code,
            'role_display': role_display,
            'count': role_data['count']
        })
    
    # Get all roles for filter dropdown
    roles = UserRole.ROLE_CHOICES
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'roles': roles,
        'total_users': total_users,
        'active_users': active_users,
        'new_today': new_today,
        'admin_users': admin_users,
        'teacher_users': teacher_users,
        'student_users': student_users,
        'role_stats': role_stats,
    }
    return render(request, 'core/admin_manage_users_professional.html', context)

@login_required
def admin_create_user(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone')
        village = request.POST.get('village')
        address = request.POST.get('address')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == '1'
        
        # Split full name into first and last name
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('admin_manage_users')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('admin_manage_users')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('admin_manage_users')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        
        # Set is_staff and is_superuser based on role
        if role == 'administrator':
            user.is_staff = True
            user.is_superuser = True
        
        user.save()
        
        # Create user role
        UserRole.objects.create(
            user=user,
            role=role,
            phone=phone,
            village=village,
            address=address
        )
        
        messages.success(request, f'User {username} created successfully!')
        return redirect('admin_manage_users')
    
    # Get all roles for the form
    roles = UserRole.ROLE_CHOICES
    
    context = {
        'roles': roles,
    }
    return render(request, 'core/admin_create_user.html', context)

@login_required
def admin_edit_user(request, user_id):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    from django.shortcuts import get_object_or_404
    user = get_object_or_404(User, id=user_id)
    user_role = getattr(user, 'role', None)
    
    if request.method == 'POST':
        # Update user details
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()
        
        # Update or create user role
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        village = request.POST.get('village')
        address = request.POST.get('address')
        
        if user_role:
            user_role.role = role
            user_role.phone = phone
            user_role.village = village
            user_role.address = address
            user_role.save()
        else:
            UserRole.objects.create(
                user=user,
                role=role,
                phone=phone,
                village=village,
                address=address
            )
        
        # Update password if provided
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
        
        messages.success(request, f'User {user.username} updated successfully!')
        return redirect('admin_manage_users')
    
    context = {
        'edit_user': user,
        'user_role': user_role,
        'roles': UserRole.ROLE_CHOICES,
    }
    return render(request, 'core/admin_edit_user.html', context)

@login_required
def admin_delete_user(request, user_id):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    from django.shortcuts import get_object_or_404
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('admin_manage_users')
    
    username = user.username
    user.delete()
    messages.success(request, f'User {username} deleted successfully!')
    return redirect('admin_manage_users')

@login_required
def admin_settings(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        # Handle settings update
        messages.success(request, 'Settings updated successfully!')
        return redirect('admin_settings')
    
    context = {
        'active_tab': request.GET.get('tab', 'general'),
    }
    return render(request, 'core/admin_settings_professional.html', context)

# Public information pages
def about_us(request):
    context = {
        'page_title': 'About Us',
    }
    return render(request, 'core/about_us.html', context)

def privacy_policy(request):
    context = {
        'page_title': 'Privacy Policy',
    }
    return render(request, 'core/privacy_policy.html', context)

def terms_of_service(request):
    context = {
        'page_title': 'Terms of Service',
    }
    return render(request, 'core/terms_of_service.html', context)

def faqs(request):
    context = {
        'page_title': 'Frequently Asked Questions',
    }
    return render(request, 'core/faqs.html', context)
