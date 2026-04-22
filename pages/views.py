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
years_of_experience = current_year - 2003 # ========== PRODUCTS CONFIGURATION ==========

PRODUCT_TEMPLATES = {
    'dsigner-component-tool':           'products/dsigner_component_tool.html',
    'real-time-signing-tool':           'products/real_time_signing_tool.html',
    'signing-verification-component':   'products/signing_verification_component.html',
    'dsigner-crypto-token':             'products/dsigner_crypto_token.html',
    'encryption-signing-component':     'products/encryption_signing_component.html',
    'electronic-management-system':     'products/electronic_management_system.html',
    'bulk-signing-component':           'products/bulk_signing_component.html',
    'optical-character-recognition':    'products/optical_character_recognition.html',
    'lakshya-micro-banking':            'products/lakshya_micro_banking.html',
    'cms-tours-travels':                'products/cms_tours_travels.html',
    'ecommerce-websites':               'products/ecommerce_websites.html',
}

PRODUCT_TITLES = {
    'dsigner-component-tool':           'DSigner Component Tool',
    'real-time-signing-tool':           'Real Time Signing Tool for Insurance Online Policy',
    'signing-verification-component':   'Signing and Verification Component (Soft Token)',
    'dsigner-crypto-token':             'DSigner (Crypto-Token)',
    'encryption-signing-component':     'Encryption Signing Component Tools',
    'electronic-management-system':     'Electronic Management System',
    'bulk-signing-component':           'Bulk Signing Component Tool',
    'optical-character-recognition':    'Optical Character Recognition Tool',
    'lakshya-micro-banking':            'Lakshya Micro Banking Software',
    'cms-tours-travels':                'CMS for Tours and Travels',
    'ecommerce-websites':               'Ecommerce Websites',
}

PRODUCT_DESCRIPTIONS = {
    'dsigner-component-tool': 'Automates signing of PDF documents and embedded form data via API with support for dynamic form data input and field-level signing.',
    'real-time-signing-tool': 'Fulfills scope for signing documents/data on real time using digital signature certificates for insurance policies.',
    'signing-verification-component': 'Supports making any application PKI enabled for using DSc issued in Soft Token with secure digital identity verification.',
    'dsigner-crypto-token': 'Supports making any application PKI enabled for using DSc issued in Crypto Token with blockchain integration.',
    'encryption-signing-component': 'Makes application and business process compatible for using digital signature certificates with encryption/decryption.',
    'electronic-management-system': 'Centralized storage and management of digital documents with version control and audit trails.',
    'bulk-signing-component': 'Supports management of document flow and archival of documents with batch signing capabilities.',
    'optical-character-recognition': 'Accurately converts scanned documents and images into editable text with AI-based algorithms.',
    'lakshya-micro-banking': 'Comprehensive management of microfinance operations and customer accounts for loans, deposits, and reports.',
    'cms-tours-travels': 'Complete control over tour packages, reservations, and customer records with integrated CRM.',
    'ecommerce-websites': 'Advanced product management, seamless checkout, inventory management, and secure transactions.',
}

PRODUCT_FEATURES = {
    'dsigner-component-tool': [
        'Supports dynamic form data input and field-level signing within PDFs',
        'Allows bulk signing of multiple documents in a single operation',
        'Real-time status and feedback via API response',
        'Securely integrates with external APIs',
        'Handles static and interactive PDF forms efficiently',
        'Configurable signature placement and appearance',
        'Seamless integration with Windows environment',
    ],
    'real-time-signing-tool': [
        'Automates signing of insurance documents and policy forms via API',
        'Ensures compliance with regulatory standards',
        'Supports dynamic form data input and field-level signing within insurance PDFs',
        'Handles static and interactive insurance forms, including claims and policy documents',
        'Allows bulk signing of multiple insurance documents',
        'Customizable signature placement and appearance',
        'Real-time status updates and feedback via API',
        'Integrates with Windows and insurance management systems',
        'Document validation and verification for authenticity',
    ],
    'signing-verification-component': [
        'Streamlined online company registration with soft-token authentication',
        'Secure digital identity verification and document signing',
        'Easy integration with registration authorities and compliance systems',
        'Supports digital signing of registration forms',
        'Real-time validation and submission',
        'Secure storage of digital certificates and soft-token credentials',
        'Customizable workflows',
        'User-friendly interface',
    ],
    'dsigner-crypto-token': [
        'Online company registration with crypto-token-based authentication',
        'Secure and decentralized identity verification',
        'Integrates with blockchain technology',
        'Supports digital signing of registration forms and compliance documents',
        'Real-time application validation and submission using blockchain ledger',
        'Secure management of crypto-tokens and digital assets',
        'Customizable registration workflows',
        'Advanced tracking and reporting features',
    ],
    'encryption-signing-component': [
        'Encrypt and decrypt PDF files with advanced cryptography algorithms',
        'Bulk processing of multiple PDFs',
        'Supports AES-256 and RSA encryption standards',
        'Easy integration with command-line or API-based operations',
        'Enables digital signing of PDFs with secure key pairs',
        'Seamless decryption of password-protected PDF files',
        'Verify authenticity of signed documents',
        'Detailed logs for tracking',
        'Configurable signing position and encryption settings',
    ],
    'electronic-management-system': [
        'Centralized storage and management of digital documents',
        'Organizes files with metadata, tagging, and categories',
        'Supports wide range of file formats (PDFs, Word documents, images)',
        'Version control to track document changes',
        'Compliance and audit trails',
        'Access control and user permissions',
        'Efficient search and filtering',
        'Seamless integration with external systems and APIs',
        'Automated backup and recovery',
        'Document workflows for review, approval, and archiving',
    ],
    'bulk-signing-component': [
        'Batch sign multiple PDF files simultaneously',
        'Option to overlay signatures or watermark',
        'Supports large PDF files up to 100MB',
        'Detailed logging of signed documents',
        'Integrates with digital certificates',
        'Customizable signing position on each page',
        'Fast processing times',
        'User-friendly interface',
    ],
    'optical-character-recognition': [
        'Supports PNG, JPEG, TIFF',
        'Extracts text from complex documents, including multi-page PDFs',
        'Recognizes multiple languages and scripts',
        'Batch processing for OCR on multiple files',
        'Configurable output formats (plain text, Word, searchable PDF)',
        'Seamless integration with document management systems',
        'Post-OCR editing and verification',
        'Advanced AI-based algorithms for handwritten text recognition',
    ],
    'lakshya-micro-banking': [
        'Supports loans, savings, and deposits',
        'Automated loan disbursement, collection, and repayment tracking',
        'Real-time reporting and analytics',
        'Customizable workflow management for loan processing',
        'Integrated customer management system',
        'Supports branch-level operations with multi-user access and role-based permissions',
        'Handles regulatory compliance and reporting',
        'Seamless integration with third-party systems (mobile wallets, payment gateways)',
        'Secure, cloud-based access for remote management',
    ],
    'cms-tours-travels': [
        'Offers flights, hotels, and vacation packages',
        'Automated booking confirmations, payment handling, itinerary updates',
        'Live reporting and insights',
        'Integrated CRM for client preferences and travel history',
        'Supports multi-location operations with user-specific roles',
        'Integration with payment systems and travel APIs',
        'Customizable workflows',
        'Cloud-based, secure platform',
        'Ensures compliance with industry regulations',
        'Responsive design on all platforms',
        'No device detection needed (faster loading)',
        'Manage content in one CMS',
        'Accessible for users with disabilities',
        'High performance technologies',
    ],
    'ecommerce-websites': [
        'Advanced product management with categories, attributes, variants',
        'Seamless checkout with multiple payment gateways',
        'Real-time order tracking and customer notification',
        'Customizable product catalogs and promotional campaigns',
        'Robust inventory management with automated stock updates',
        'Detailed sales analytics',
        'Customer account management with order history and wish lists',
        'Data encryption and secure transactions',
        'Integration with shipping providers and third-party services',
        'Scalable and customizable design',
        'Flexible product management',
        'Insightful sales reports and customer behavior analytics',
        'Integrated shopping cart',
        'Comprehensive order management',
        'High-level security',
        'Customizable user roles and permissions',
        'Integration with external APIs',
        'Advanced search functionality',
        'Responsive and adaptive design',
    ],
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

def products(request):
    """
    Products listing page showing all products
    """
    products_list = []
    for slug, title in PRODUCT_TITLES.items():
        products_list.append({
            'slug': slug,
            'title': title,
            'description': PRODUCT_DESCRIPTIONS.get(slug, ''),
            'features': PRODUCT_FEATURES.get(slug, [])[:3],  
        })
    
    context = {
        'title': 'Products - Radiant Infotech',
        'description': 'Explore our comprehensive range of digital products including digital signature tools, document management systems, banking software, and more.',
        'keywords': 'digital signature, document signing, OCR, micro banking, ecommerce, CMS, software products, Nepal',
        'products': products_list,
    }
    return render(request, 'pages/products.html', context)

def product_detail(request, slug):
    """
    Individual product detail page
    """
    template = PRODUCT_TEMPLATES.get(slug)
    if not template:
        raise Http404("Product not found.")
    
    context = {
        'product_slug': slug,
        'product_title': PRODUCT_TITLES.get(slug, 'Product'),
        'product_description': PRODUCT_DESCRIPTIONS.get(slug, ''),
        'product_features': PRODUCT_FEATURES.get(slug, []),
        'product_name': PRODUCT_TITLES.get(slug, 'Product'),
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
Phone: 01-4545765 , 01-4524311

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
    