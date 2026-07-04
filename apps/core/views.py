from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import io
import json
import logging
from xhtml2pdf import pisa

from .models import LoanQuotationLead, CalculatorAnalytics, UIInteractionLog, ContactUsLead, NewsletterSubscriber
from .forms import LoanQuotationLeadForm, ContactUsLeadForm, NewsletterSubscriberForm

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'core/home.html')

def personal_loan(request):
    return render(request, 'core/personal_loan.html')

def mortgage(request):
    return render(request, 'core/mortgage.html')

def credit_card(request):
    return render(request, 'core/credit_card.html')

def business_loan(request):
    return render(request, 'core/business_loan.html')

def business_account(request):
    return render(request, 'core/business_account.html')

def about_us(request):
    return render(request, 'core/about_us.html')

def become_partner(request):
    return render(request, 'core/become_partner.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')

def bdp_guides(request):
    return render(request, 'core/bdp-guides.html')    

def faq(request):
    return render(request, 'core/faq.html')

def our_leaders(request):
    return render(request, 'core/our_leaders.html')

def bdp_faq(request):
    return render(request, 'core/bdp-faq.html')    

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def calculate_emi_details(loan_amount, interest_rate, tenure_months):
    P = float(loan_amount)
    annual_rate = float(interest_rate)
    n = int(tenure_months)

    if P <= 0 or annual_rate < 0 or n <= 0:
        return 0.0, 0.0, 0.0

    r = (annual_rate / 12) / 100

    if r == 0:
        emi = P / n
    else:
        emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

    total_payment = emi * n
    total_interest = total_payment - P

    return round(emi, 2), round(P, 2), round(total_interest, 2)



def fetch_resources(uri, rel):
    import os
    from django.conf import settings
    import urllib.parse
    
    # Normalize paths
    uri = urllib.parse.unquote(uri)
    static_url = settings.STATIC_URL
    if not static_url.startswith('/'):
        static_url = '/' + static_url

    if uri.startswith(static_url):
        path = os.path.join(str(settings.STATIC_ROOT or settings.BASE_DIR / 'static'), uri.replace(static_url, ""))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(str(settings.MEDIA_ROOT), uri.replace(settings.MEDIA_URL, ""))
    else:
        path = os.path.join(str(settings.BASE_DIR), uri)
    
    # Try finding the file in STATICFILES_DIRS if not found in STATIC_ROOT
    if not os.path.isfile(path):
        for dir in settings.STATICFILES_DIRS:
            test_path = os.path.join(str(dir), uri.replace(static_url, ""))
            if os.path.isfile(test_path):
                print(f"DEBUG: Found in STATICFILES_DIRS -> {test_path}")
                return str(test_path)
    
    print(f"DEBUG: Path -> {path}, exists? {os.path.isfile(path)}")
    return str(path)

@require_POST
def generate_loan_quotation(request):
    form = LoanQuotationLeadForm(request.POST)
    if form.is_valid():
        try:
            lead = form.save()

            # Analytics event
            CalculatorAnalytics.objects.create(
                event_type='Quote Downloaded',
                metadata={
                    'lead_id': lead.id,
                    'name': lead.name,
                    'email': lead.email,
                    'product_type': lead.product_type,
                    'loan_amount': str(lead.loan_amount),
                    'interest_rate': str(lead.interest_rate),
                    'tenure': lead.tenure,
                    'emi': str(lead.emi),
                }
            )

            # Breakdown calculations for PDF
            emi, principal, interest = calculate_emi_details(
                lead.loan_amount, lead.interest_rate, lead.tenure
            )
            total_payment     = principal + interest
            principal_percent = round((principal / total_payment) * 100, 1) if total_payment > 0 else 0
            interest_percent  = round((interest  / total_payment) * 100, 1) if total_payment > 0 else 0

            # Generate PDF using WeasyPrint
            context = {
                'lead': lead,
                'emi': emi,
                'principal': principal,
                'interest': interest,
                'principal_percent': principal_percent,
                'interest_percent': interest_percent,
            }
            html_string = render_to_string('pdf/loan_quotation.html', context)
            
            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result, link_callback=fetch_resources)
            if not pdf.err:
                pdf_bytes = result.getvalue()
            else:
                raise Exception("Error generating PDF")

            safe_name = "".join([c if c.isalnum() else "_" for c in lead.name])
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = (
                f'attachment; filename="Loan_Quotation_{safe_name}.pdf"'
            )
            return response

        except Exception as e:
            logger.exception("PDF generation failed")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@require_POST
def track_calculator_event(request):
    try:
        data       = json.loads(request.body)
        event_type = data.get('event_type')
        metadata   = data.get('metadata', {})

        if event_type not in ['Calculator Opened', 'EMI Calculated', 'Quote Downloaded']:
            return JsonResponse({'error': 'Invalid event type'}, status=400)

        CalculatorAnalytics.objects.create(event_type=event_type, metadata=metadata)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

from django.http import FileResponse, Http404
from django.conf import settings
import os

def download_guide(request, filename):

    import urllib.parse
    filename = urllib.parse.unquote(filename)

    print("=" * 50)
    print("BASE_DIR =", settings.BASE_DIR)

    guide_path = os.path.join(
        settings.BASE_DIR,
        "guides",
        filename
    )

    print("Guide Path =", guide_path)
    print("Exists =", os.path.exists(guide_path))
    print("=" * 50)

    if not os.path.exists(guide_path):
        raise Http404("File not found")

    return FileResponse(
        open(guide_path, "rb"),
        as_attachment=True,
        filename=filename
    )

@require_POST
def track_ui_movement(request):
    try:
        data = json.loads(request.body)
        element_id = data.get('element_id')
        event_type = data.get('event_type')
        page_url = data.get('page_url')
        metadata = data.get('metadata', {})
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            
        UIInteractionLog.objects.create(
            user_session_id=session_key,
            element_id=element_id,
            event_type=event_type,
            page_url=page_url,
            metadata=metadata
        )
        return JsonResponse({'success': True})
    except Exception as e:
        logger.exception("UI tracking failed")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def submit_contact_us(request):
    form = ContactUsLeadForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@require_POST
def subscribe_newsletter(request):
    form = NewsletterSubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


    