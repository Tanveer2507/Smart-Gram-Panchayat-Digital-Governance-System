from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q
from django.utils import timezone
from .models import BudgetRecord, ExpenseEntry
from notifications.models import AdminNotification
from django.contrib.auth.models import User
from decimal import Decimal
import datetime

def budget_dashboard(request):
    records = BudgetRecord.objects.all()
    
    total_budget = records.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    total_spent = records.aggregate(Sum('spent_amount'))['spent_amount__sum'] or 0
    
    department_data = []
    for dept_code, dept_name in BudgetRecord.DEPARTMENT_CHOICES:
        dept_records = records.filter(department=dept_code)
        dept_total = dept_records.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
        department_data.append({
            'name': dept_name,
            'amount': dept_total
        })
    
    context = {
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining': total_budget - total_spent,
        'records': records[:10],
        'department_data': department_data,
    }
    return render(request, 'budget/dashboard.html', context)


@login_required
def admin_manage_budget(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Handle POST requests for add/edit/delete
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            try:
                # Get form data
                department = request.POST.get('department')
                title = request.POST.get('title')
                description = request.POST.get('description', '')
                allocated_amount = request.POST.get('allocated_amount')
                financial_year = request.POST.get('financial_year')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                
                # Validate required fields
                if not all([department, title, allocated_amount, financial_year]):
                    messages.error(request, 'Please fill all required fields!')
                    return redirect('admin_manage_budget')
                
                # Create budget record
                budget = BudgetRecord.objects.create(
                    department=department,
                    title=title,
                    description=description,
                    allocated_amount=Decimal(allocated_amount),
                    financial_year=financial_year,
                    start_date=start_date if start_date else None,
                    end_date=end_date if end_date else None,
                    created_by=request.user,
                )
                budget.update_status()
                
                # Create notification for all admin users
                admin_users = User.objects.filter(is_staff=True, is_superuser=True)
                for admin in admin_users:
                    AdminNotification.objects.create(
                        user=admin,
                        title='New Budget Created',
                        message=f'Budget "{title}" for {budget.get_department_display()} has been created with allocated amount of ₹{allocated_amount} for {financial_year}.',
                        notification_type='budget',
                        related_link='/budget/admin-manage/',
                    )
                
                messages.success(request, 'Budget created successfully!')
                return redirect('admin_manage_budget')
            except Exception as e:
                messages.error(request, f'Error creating budget: {str(e)}')
                return redirect('admin_manage_budget')
        
        elif action == 'edit':
            try:
                budget_id = request.POST.get('budget_id')
                budget = get_object_or_404(BudgetRecord, id=budget_id)
                
                # Update fields
                budget.department = request.POST.get('department')
                budget.title = request.POST.get('title')
                budget.description = request.POST.get('description', '')
                budget.allocated_amount = Decimal(request.POST.get('allocated_amount'))
                budget.financial_year = request.POST.get('financial_year')
                
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                budget.start_date = start_date if start_date else None
                budget.end_date = end_date if end_date else None
                
                budget.save()
                budget.update_status()
                
                # Create notification for all admin users
                admin_users = User.objects.filter(is_staff=True, is_superuser=True)
                for admin in admin_users:
                    AdminNotification.objects.create(
                        user=admin,
                        title='Budget Updated',
                        message=f'Budget "{budget.title}" for {budget.get_department_display()} has been updated.',
                        notification_type='budget',
                        related_link='/budget/admin-manage/',
                    )
                
                messages.success(request, 'Budget updated successfully!')
                return redirect('admin_manage_budget')
            except Exception as e:
                messages.error(request, f'Error updating budget: {str(e)}')
                return redirect('admin_manage_budget')
        
        elif action == 'add_expense':
            try:
                budget_id = request.POST.get('budget_id')
                budget = get_object_or_404(BudgetRecord, id=budget_id)
                
                # Get expense data
                expense_title = request.POST.get('expense_title')
                expense_amount = Decimal(request.POST.get('expense_amount'))
                expense_category = request.POST.get('expense_category')
                expense_date = request.POST.get('expense_date')
                expense_remarks = request.POST.get('expense_remarks', '')
                
                # Create expense entry
                expense = ExpenseEntry.objects.create(
                    budget=budget,
                    title=expense_title,
                    amount=expense_amount,
                    category=expense_category,
                    date=expense_date,
                    remarks=expense_remarks,
                    created_by=request.user,
                )
                
                # Handle file upload
                if request.FILES.get('expense_receipt'):
                    expense.receipt = request.FILES['expense_receipt']
                    expense.save()
                
                # Update budget spent amount
                budget.spent_amount += expense.amount
                budget.save()
                budget.update_status()
                
                # Create notification for all admin users
                admin_users = User.objects.filter(is_staff=True, is_superuser=True)
                for admin in admin_users:
                    AdminNotification.objects.create(
                        user=admin,
                        title='New Expense Added',
                        message=f'Expense "{expense_title}" of ₹{expense_amount} has been added to budget "{budget.title}". Current utilization: {budget.utilization_percentage:.1f}%',
                        notification_type='budget',
                        related_link='/budget/admin-manage/',
                    )
                
                messages.success(request, 'Expense entry added successfully!')
                return redirect('admin_manage_budget')
            except Exception as e:
                messages.error(request, f'Error adding expense: {str(e)}')
                return redirect('admin_manage_budget')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    status_filter = request.GET.get('status', '')
    department_filter = request.GET.get('department', '')
    
    # Get all budgets
    budgets = BudgetRecord.objects.all().select_related('created_by').order_by('-created_at')
    
    # Update statuses
    for budget in budgets:
        budget.update_status()
    
    # Apply filters
    if search_query:
        budgets = budgets.filter(Q(title__icontains=search_query) | Q(department__icontains=search_query))
    
    if year_filter:
        budgets = budgets.filter(financial_year=year_filter)
    
    if status_filter:
        budgets = budgets.filter(status=status_filter)
    
    if department_filter:
        budgets = budgets.filter(department=department_filter)
    
    # Calculate statistics
    total_allocated = BudgetRecord.objects.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    total_utilized = BudgetRecord.objects.aggregate(Sum('spent_amount'))['spent_amount__sum'] or 0
    total_remaining = total_allocated - total_utilized
    active_projects = BudgetRecord.objects.filter(status__in=['on_track', 'near_limit']).count()
    over_budget_projects = BudgetRecord.objects.filter(status='over_budget').count()
    
    # Get unique financial years
    financial_years = BudgetRecord.objects.values_list('financial_year', flat=True).distinct().order_by('-financial_year')
    
    context = {
        'budgets': budgets,
        'search_query': search_query,
        'year_filter': year_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'total_allocated': total_allocated,
        'total_utilized': total_utilized,
        'total_remaining': total_remaining,
        'active_projects': active_projects,
        'over_budget_projects': over_budget_projects,
        'financial_years': financial_years,
        'departments': BudgetRecord.DEPARTMENT_CHOICES,
        'today': datetime.date.today().isoformat(),
    }
    return render(request, 'budget/admin_manage_budget_professional.html', context)


@login_required
@require_http_methods(["GET"])
def budget_api_detail(request, pk):
    """API endpoint for fetching budget details"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    budget = get_object_or_404(BudgetRecord, pk=pk)
    
    # Get expense entries
    expenses = budget.expenses.all()
    expense_list = [{
        'id': exp.id,
        'title': exp.title,
        'amount': float(exp.amount),
        'category': exp.category,
        'category_display': exp.get_category_display(),
        'date': exp.date.strftime('%Y-%m-%d'),
        'remarks': exp.remarks or '',
        'receipt_url': exp.receipt.url if exp.receipt else None,
    } for exp in expenses]
    
    data = {
        'id': budget.id,
        'title': budget.title,
        'department': budget.department,
        'department_display': budget.get_department_display(),
        'description': budget.description or '',
        'allocated_amount': float(budget.allocated_amount),
        'spent_amount': float(budget.spent_amount),
        'remaining_amount': float(budget.remaining_amount),
        'utilization_percentage': round(budget.utilization_percentage, 2),
        'financial_year': budget.financial_year,
        'start_date': budget.start_date.strftime('%Y-%m-%d') if budget.start_date else None,
        'end_date': budget.end_date.strftime('%Y-%m-%d') if budget.end_date else None,
        'status': budget.status,
        'status_display': budget.get_status_display(),
        'created_by': budget.created_by.username if budget.created_by else 'Unknown',
        'created_at': budget.created_at.strftime('%B %d, %Y'),
        'updated_at': budget.updated_at.strftime('%B %d, %Y'),
        'expenses': expense_list,
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def budget_api_delete(request, pk):
    """API endpoint for deleting budgets"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    budget = get_object_or_404(BudgetRecord, pk=pk)
    budget_title = budget.title
    budget_dept = budget.get_department_display()
    
    budget.delete()
    
    # Create notification for all admin users
    admin_users = User.objects.filter(is_staff=True, is_superuser=True)
    for admin in admin_users:
        AdminNotification.objects.create(
            user=admin,
            title='Budget Deleted',
            message=f'Budget "{budget_title}" for {budget_dept} has been deleted.',
            notification_type='budget',
            related_link='/budget/admin-manage/',
        )
    
    return JsonResponse({'success': True, 'message': 'Budget deleted successfully'})
