from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import threading
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.utils import timezone
import re
from django.http import HttpResponse, JsonResponse, Http404
from datetime import datetime
import os

SERVICE_TEMPLATES = {
    'digital-marketing':  'services/digital_marketing.html',
    'digital-signature':  'services/digital_signature.html',
    'ict-support':        'services/ict_support.html',
    'mis-solutions':       'services/mis_solutions.html',

    'web-development':    'services/web_development.html',
    'software-development':'services/software_development.html',
    'mobile-applications':'services/mobile_applications.html',
    'cloud-services':     'services/cloud_services.html',
    'graphics-designing': 'services/graphics_designing.html',
    'data-entry':         'services/data_entry.html',
}
 
SERVICE_TITLES = {
    'digital-marketing':   'Digital Marketing',
    'mis-solutions':       'MIS Solutions',
    'software-development':'Software Development',
    'ict-support':        'ICT Support',
    'digital-signature':   'Digital Signature',
    'web-development':     'Web Development',
    'mobile-applications': 'Mobile Applications',
    'cloud-services':      'Cloud Services',
    'graphics-designing':  'Graphics Designing',
    'data-entry':          'Data Entry',
}
current_year = datetime.now().year
years_of_experience = current_year - 2003 

def home(request):
    
    context = {
        'title': 'Home - Radiant Infotech',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/home.html', context)

def about_us(request):
    
    context = {
        'title': 'About Us',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/about_us.html', context)

def services(request):
    
    context = {
        'title': 'Services - Radiant Infotech',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/services.html', context)

def service_detail(request, slug):
    template = SERVICE_TEMPLATES.get(slug)
    if not template:
        raise Http404("Service not found.")
 
    context = {
        'service_slug':  slug,
        'service_title': SERVICE_TITLES.get(slug, 'Service'),
    }
    return render(request, template, context)

def gallery(request):
    
    context = {
        'title': 'Home - Radiant Infotech',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/gallery.html', context)

def career(request):
    
    context = {
        'title': 'Career - Radiant Infotech',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/career.html', context)

def contact_us(request):
    
    context = {
        'title': 'Home - Radiant Infotech',
        'description': 'Welcome to Radiant Infotech, your trusted partner for software development and digital signature solutions.',
        'keywords': 'home, radiant infotech, software development, digital signature, web development, mobile apps, e-signature',
    }
    return render(request, 'pages/contact_us.html', context)



def view_404(request, exception=None):
    return render(request, 'pages/404.html', status=404)

def send_contact_email(form_data, file_data=None):
    """
    Send emails to admin and user for Radiant Infotech Pvt. Ltd contact form with attachment support
    """
    try:
        # Prepare admin email with attachment
        admin_subject = f"New Contact Form Inquiry - Radiant Infotech Pvt. Ltd Website"
        admin_message = f"""
New Contact Form Submission from Radiant Infotech Pvt. Ltd Website:

Name: {form_data.get('name')}
Email: {form_data.get('email')}
Subject: {form_data.get('subject')}

Message:
{form_data.get('message')}

Submitted on: {form_data.get('timestamp', 'Now')}

This inquiry was submitted through the Radiant Infotech website.
        """
        
        # Create email with attachment for admin
        admin_email = EmailMessage(
            subject=admin_subject,
            body=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        
        if file_data:
            admin_email.attach(
                file_data['filename'],
                file_data['content'],
                file_data['content_type']
            )
        
        admin_email.send(fail_silently=False)
        
        user_subject = "Thank You for Your Inquiry - Radiant Infotech Pvt. Ltd"
        user_message = f"""
Dear {form_data.get('name')},

Thank you for reaching out to Radiant Infotech Pvt. Ltd. We have received your inquiry and our team will get back to you within 24 hours on business days.

Here's a summary of your inquiry:
- Subject: {form_data.get('subject')}
- Submitted: {form_data.get('timestamp', 'Now')}

{'Attached file: ' + file_data['filename'] if file_data else ''}

For urgent inquiries, please contact us at:
Email: {settings.DEFAULT_FROM_EMAIL}
Phone: +91-XXXXXXXXXX

Best regards,
Radiant Infotech Pvt. Ltd Team
Your Trusted Technology Partner
        """
        
        user_email_addr = form_data.get('email')
        if user_email_addr:
            user_email = EmailMessage(
                subject=user_subject,
                body=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email_addr],
            )
            user_email.send(fail_silently=False)
            
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"Error sending email: {e}")


@csrf_exempt
@require_POST
def contact_submit(request):
    """
    Handle contact form submission with file attachment and send emails for Radiant Infotech Pvt. Ltd
    """
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)
        
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            }, status=400)
        
        form_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            'company': "Radiant Infotech Pvt. Ltd"
        }
        
        file_data = None
        if 'attachment' in request.FILES:
            uploaded_file = request.FILES['attachment']
            
            if uploaded_file.size > 10 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'message': 'File size must be less than 10MB.'
                }, status=400)
            
            allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt', '.zip']
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext not in allowed_extensions:
                return JsonResponse({
                    'success': False,
                    'message': 'File type not allowed. Please upload PDF, DOC, DOCX, JPG, PNG, TXT, or ZIP files.'
                }, status=400)
            
            file_data = {
                'filename': uploaded_file.name,
                'content': uploaded_file.read(),
                'content_type': uploaded_file.content_type or 'application/octet-stream'
            }
        
        email_thread = threading.Thread(
            target=send_contact_email,
            args=(form_data, file_data)
        )
        email_thread.daemon = True
        email_thread.start()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for contacting Radiant Infotech Pvt. Ltd! We have received your inquiry and will get back to you within 24 hours. A confirmation email has been sent to your email address.'
        })
        
    except Exception as e:
        print(f"Error in contact_submit: {e}")
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)
    