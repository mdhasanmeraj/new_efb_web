from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('personal-loan/', views.personal_loan, name='personal_loan'),
    path('mortgage/', views.mortgage, name='mortgage'),
    path('credit-card/', views.credit_card, name='credit_card'),
    path('business-loan/', views.business_loan, name='business_loan'),
    path('business-account/', views.business_account, name='business_account'),
    path('about/', views.about_us, name='about_us'),
    path('partner/', views.become_partner, name='become_partner'),
    path('contact/', views.contact_us, name='contact_us'),
    path('faq/', views.faq, name='faq'),
    path('our-leaders/', views.our_leaders, name='our_leaders'),
    path('generate-loan-quotation/', views.generate_loan_quotation, name='generate_loan_quotation'),
    path('track-calculator-event/', views.track_calculator_event, name='track_calculator_event'),
    path('track-ui-movement/', views.track_ui_movement, name='track_ui_movement'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('bdp-guides/', views.bdp_guides, name='bdp_guides'), 
    path('bdp-faq/', views.bdp_faq, name='bdp_faq'), 
    re_path(r'^download-guide/(?P<filename>[\w\s\.\-_%]+)/?$', views.download_guide, name='download_guide'),
    path("submit-enquiry/",views.submit_enquiry,name="submit_enquiry",),
    path("submit-consultation/",views.submit_consultation,name="submit_consultation",),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt",content_type="text/plain",),name="robots_txt", ),

]
