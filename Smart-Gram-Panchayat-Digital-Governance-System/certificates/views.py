from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone
from .models import Certificate
import random
import string
import datetime

def certificate_list(request):
    certificates = Certificate.objects.all()
    if request.user.is_authenticated:
        user_certificates = certificates.filter(user=request.user)
    else:
        user_certificates = []
    
    context = {
        'certificates': certificates[:10],
        'user_certificates': user_certificates,
    }
    return render(request, 'certificates/list.html', context)

@login_required
def certificate_create(request):
    if request.method == 'POST':
        app_number = 'CERT' + ''.join(random.choices(string.digits, k=8))
        certificate = Certificate.objects.create(
            user=request.user,
            certificate_type=request.POST.get('certificate_type'),
            applicant_name=request.POST.get('applicant_name'),
            father_name=request.POST.get('father_name'),
            address=request.POST.get('address'),
            purpose=request.POST.get('purpose'),
            application_number=app_number,
        )
        if request.FILES.get('document'):
            certificate.document = request.FILES['document']
            certificate.save()
        messages.success(request, f'Application submitted! Your application number: {app_number}')
        return redirect('certificate_list')
    return render(request, 'certificates/create.html')

@login_required
def certificate_detail(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    return render(request, 'certificates/detail.html', {'certificate': certificate})


@login_required
def admin_manage_certificates(request):
    # Check if user is admin
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Handle POST requests for add/edit/approve/reject/issue/verify
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Generate application number if not provided
            app_number = request.POST.get('application_number')
            if not app_number:
                app_number = 'CERT' + ''.join(random.choices(string.digits, k=8))
            
            certificate = Certificate.objects.create(
                user=request.user,
                certificate_type=request.POST.get('certificate_type'),
                applicant_name=request.POST.get('applicant_name'),
                father_name=request.POST.get('father_name'),
                address=request.POST.get('address'),
                purpose=request.POST.get('purpose'),
                application_number=app_number,
                status=request.POST.get('status', 'pending'),
                remarks=request.POST.get('remarks', ''),
            )
            if request.FILES.get('document'):
                certificate.document = request.FILES['document']
                certificate.save()
            messages.success(request, 'Certificate request created successfully!')
            return redirect('admin_manage_certificates')
        
        elif action == 'edit':
            certificate_id = request.POST.get('certificate_id')
            certificate = get_object_or_404(Certificate, id=certificate_id)
            certificate.applicant_name = request.POST.get('applicant_name')
            certificate.father_name = request.POST.get('father_name')
            certificate.certificate_type = request.POST.get('certificate_type')
            certificate.address = request.POST.get('address')
            certificate.purpose = request.POST.get('purpose')
            certificate.status = request.POST.get('status')
            certificate.remarks = request.POST.get('remarks', '')
            certificate.save()
            messages.success(request, 'Certificate updated successfully!')
            return redirect('admin_manage_certificates')
        
        elif action == 'approve':
            certificate_id = request.POST.get('certificate_id')
            certificate = get_object_or_404(Certificate, id=certificate_id)
            certificate.status = 'approved'
            certificate.approved_by = request.user
            certificate.approved_date = timezone.now()
            remarks = request.POST.get('remarks', '')
            if remarks:
                certificate.remarks = remarks
            certificate.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='Certificate Approved',
                    message=f'Certificate for "{certificate.applicant_name}" has been approved by {request.user.username}.',
                    notification_type='certificate',
                    related_link='/certificates/admin/manage/'
                )
            
            messages.success(request, 'Certificate approved successfully!')
            return redirect('admin_manage_certificates')
        
        elif action == 'reject':
            certificate_id = request.POST.get('certificate_id')
            certificate = get_object_or_404(Certificate, id=certificate_id)
            certificate.status = 'rejected'
            certificate.remarks = request.POST.get('remarks', '')
            certificate.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='Certificate Rejected',
                    message=f'Certificate for "{certificate.applicant_name}" has been rejected by {request.user.username}.',
                    notification_type='certificate',
                    related_link='/certificates/admin/manage/'
                )
            
            messages.error(request, 'Certificate rejected.')
            return redirect('admin_manage_certificates')
        
        elif action == 'issue':
            certificate_id = request.POST.get('certificate_id')
            certificate = get_object_or_404(Certificate, id=certificate_id)
            certificate.status = 'issued'
            issue_date = request.POST.get('issue_date')
            if issue_date:
                certificate.issue_date = issue_date
            remarks = request.POST.get('remarks', '')
            if remarks:
                certificate.remarks = remarks
            if request.FILES.get('signature'):
                certificate.digital_signature = request.FILES['signature']
            certificate.save()
            
            # Create notification for all admins
            from notifications.models import AdminNotification
            from django.contrib.auth.models import User
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            for admin in admin_users:
                AdminNotification.objects.create(
                    user=admin,
                    title='Certificate Issued',
                    message=f'Certificate for "{certificate.applicant_name}" has been issued by {request.user.username}.',
                    notification_type='certificate',
                    related_link='/certificates/admin/manage/'
                )
            
            messages.success(request, 'Certificate issued successfully!')
            return redirect('admin_manage_certificates')
        
        elif action == 'verify':
            certificate_id = request.POST.get('certificate_id')
            certificate = get_object_or_404(Certificate, id=certificate_id)
            certificate.verification_status = request.POST.get('verification_status')
            certificate.status = request.POST.get('status', 'under_review')
            remarks = request.POST.get('remarks', '')
            if remarks:
                certificate.remarks = remarks
            certificate.save()
            messages.success(request, 'Verification completed successfully!')
            return redirect('admin_manage_certificates')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('certificate_type', '')
    status_filter = request.GET.get('status', '')
    
    # Get all certificates
    certificates = Certificate.objects.all().select_related('user', 'approved_by').order_by('-created_at')
    
    # Apply filters
    if search_query:
        certificates = certificates.filter(
            Q(applicant_name__icontains=search_query) |
            Q(application_number__icontains=search_query)
        )
    
    if type_filter:
        certificates = certificates.filter(certificate_type=type_filter)
    
    if status_filter:
        certificates = certificates.filter(status=status_filter)
    
    # Calculate statistics
    total_certificates = Certificate.objects.count()
    pending_certificates = Certificate.objects.filter(status='pending').count()
    approved_certificates = Certificate.objects.filter(status='approved').count()
    rejected_certificates = Certificate.objects.filter(status='rejected').count()
    issued_certificates = Certificate.objects.filter(status='issued').count()
    
    context = {
        'certificates': certificates,
        'search_query': search_query,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'total_certificates': total_certificates,
        'pending_certificates': pending_certificates,
        'approved_certificates': approved_certificates,
        'rejected_certificates': rejected_certificates,
        'issued_certificates': issued_certificates,
        'today': datetime.date.today().isoformat(),
    }
    return render(request, 'certificates/admin_manage_certificates_professional.html', context)


@login_required
@require_http_methods(["GET"])
def certificate_api_detail(request, pk):
    """API endpoint for fetching certificate details"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    certificate = get_object_or_404(Certificate, pk=pk)
    
    data = {
        'id': certificate.id,
        'application_number': certificate.application_number,
        'certificate_type': certificate.certificate_type,
        'certificate_type_display': certificate.get_certificate_type_display(),
        'applicant_name': certificate.applicant_name,
        'father_name': certificate.father_name,
        'address': certificate.address,
        'purpose': certificate.purpose,
        'status': certificate.status,
        'status_display': certificate.get_status_display(),
        'remarks': certificate.remarks or '',
        'created_at': certificate.created_at.strftime('%B %d, %Y'),
        'updated_at': certificate.updated_at.strftime('%B %d, %Y'),
        'user_name': certificate.user.get_full_name() or certificate.user.username,
        'approved_by': certificate.approved_by.username if certificate.approved_by else None,
        'approved_date': certificate.approved_date.strftime('%B %d, %Y') if certificate.approved_date else None,
        'issue_date': certificate.issue_date.strftime('%B %d, %Y') if certificate.issue_date else None,
        'document_url': certificate.document.url if certificate.document else None,
        'signature_url': certificate.digital_signature.url if certificate.digital_signature else None,
        'verification_status': certificate.verification_status or '',
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def certificate_api_delete(request, pk):
    """API endpoint for deleting certificates"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.delete()
    
    return JsonResponse({'success': True, 'message': 'Certificate deleted successfully'})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

@login_required
def certificate_download(request, pk):
    """Generate and download certificate PDF"""
    certificate = get_object_or_404(Certificate, pk=pk)
    
    # Check if user has permission to download
    if not (request.user == certificate.user or request.user.is_staff):
        messages.error(request, 'You do not have permission to download this certificate.')
        return redirect('certificate_list')
    
    # Check if certificate is approved or issued
    if certificate.status not in ['approved', 'issued']:
        messages.error(request, 'Certificate must be approved before downloading.')
        return redirect('certificate_list')
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#f97316'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
    )
    
    center_style = ParagraphStyle(
        'CustomCenter',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    
    # Add header
    elements.append(Paragraph("SMART GRAM PANCHAYAT", title_style))
    elements.append(Paragraph("DIGITAL GOVERNANCE SYSTEM", heading_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Certificate title
    cert_title = certificate.get_certificate_type_display().upper()
    elements.append(Paragraph(f"<b>{cert_title}</b>", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Certificate number
    elements.append(Paragraph(f"<b>Certificate No:</b> {certificate.application_number}", center_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Certificate content
    elements.append(Paragraph("This is to certify that:", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Create table for details
    data = [
        ['Applicant Name:', certificate.applicant_name],
        ['Father\'s Name:', certificate.father_name],
        ['Address:', certificate.address],
        ['Purpose:', certificate.purpose],
    ]
    
    if certificate.issue_date:
        data.append(['Issue Date:', certificate.issue_date.strftime('%B %d, %Y')])
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Status
    if certificate.status == 'issued':
        elements.append(Paragraph(f"<b>Status:</b> ISSUED", normal_style))
    else:
        elements.append(Paragraph(f"<b>Status:</b> APPROVED", normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Approved by
    if certificate.approved_by:
        elements.append(Paragraph(f"<b>Approved By:</b> {certificate.approved_by.get_full_name() or certificate.approved_by.username}", normal_style))
    
    if certificate.approved_date:
        elements.append(Paragraph(f"<b>Approved Date:</b> {certificate.approved_date.strftime('%B %d, %Y')}", normal_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Digital signature placeholder
    if certificate.digital_signature:
        elements.append(Paragraph("<b>Digital Signature:</b>", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        # Note: In production, you would add the actual signature image here
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("_" * 50, center_style))
    elements.append(Paragraph("<b>Authorized Signatory</b>", center_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("This is a computer-generated certificate and does not require a physical signature.", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.application_number}.pdf"'
    response.write(pdf)
    
    return response
