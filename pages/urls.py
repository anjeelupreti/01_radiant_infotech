from django.urls import path 
from .views import *

urlpatterns = [
    # Homepage
    path('', home, name='home'), 
    path('about_us/', about_us, name='about_us'), 
    path('services/', services, name='services'), 
    path('services/<slug:slug>/',service_detail, name='service_detail'),
    path('products/', products, name='products'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('gallery/', gallery, name='gallery'), 
    path('career/', career, name='career'), 
    path('contact_us', contact_us, name='contact_us'),
    path('contact-submit/', contact_submit, name='contact_submit'),
]