from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import threading
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.utils import timezone
import re
from django.http import HttpResponse, JsonResponse, Http404


SERVICE_TEMPLATES = {
    'digital-signature':  'services/digital_signature.html',
    'web-development':    'services/web_development.html',
    'mobile-applications':'services/mobile_applications.html',
    'cloud-services':     'services/cloud_services.html',
    'graphics-designing': 'services/graphics_designing.html',
    'data-entry':         'services/data_entry.html',
}
 
SERVICE_TITLES = {
    'digital-signature':   'Digital Signature',
    'web-development':     'Web Development',
    'mobile-applications': 'Mobile Applications',
    'cloud-services':      'Cloud Services',
    'graphics-designing':  'Graphics Designing',
    'data-entry':          'Data Entry',
}
 

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

def send_contact_emails(form_data):
    """
    Send emails to admin and user for Radiant Infotech Pvt. Ltd contact form
    """
    try:
        # Email to admin
        admin_subject = f"New Contact Form Inquiry - Radiant Infotech Pvt. Ltd Website"
        admin_message = f"""
        New Contact Form Submission from Radiant Infotech Pvt. Ltd Website:
        
        Name: {form_data.get('name')}
        Email: {form_data.get('email')}
        Subject: {form_data.get('subject')}
        
        Message:
        {form_data.get('message')}
        
        Submitted on: {form_data.get('timestamp', 'Now')}
        
        Product Inquiry from Distributor Website
        """
        
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        # Email to user
        user_subject = "Thank You for Your Inquiry - Radiant Infotech Pvt. Ltd"
        user_message = f"""
        Dear {form_data.get('name')},
        
        Thank you for reaching out to Radiant Infotech Pvt. Ltd. We have received your inquiry and our team will get back to you within 24 hours on business days with pricing and availability information.
        
        Here's a summary of your inquiry:
        - Subject: {form_data.get('subject')}
        - Submitted: {form_data.get('timestamp', 'Now')}
        
        For urgent inquiries, please contact us at:
        Email: support@sambhavitrading.com
        Phone: +XX XXXXXXXX
        
        Best regards,
        Radiant Infotech Pvt. Ltd Team
        Your Trusted Distribution Partner
        """
        
        user_email = form_data.get('email')
        if user_email:
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"Error sending email: {e}")


@csrf_exempt
@require_POST
def contact_submit(request):
    """
    Handle contact form submission and send emails for Radiant Infotech Pvt. Ltd
    """
    try:
        # Decode request body with UTF-8 encoding
        data = json.loads(request.body.decode('utf-8'))
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Please fill in the {field.replace("_", " ")} field.'
                }, status=400)
        
        # Validate email format with regex
        email = data.get('email', '')
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            }, status=400)
        
        # Add timestamp
        data['timestamp'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add company info
        data['company'] = "Radiant Infotech Pvt. Ltd"
        
        # Send emails in background thread
        email_thread = threading.Thread(target=send_contact_emails, args=(data,))
        email_thread.start()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for contacting Radiant Infotech Pvt. Ltd! We have received your inquiry and will get back to you within 24 hours with pricing and product information. A confirmation email has been sent to your email address.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid form data.'
        }, status=400)
    except UnicodeDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid encoding in form data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)