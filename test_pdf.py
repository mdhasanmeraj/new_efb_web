import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from core.models import LoanQuotationLead
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io


try:
    lead = LoanQuotationLead.objects.first()
    if not lead:
        lead = LoanQuotationLead.objects.create(name="Test", mobile="123", email="t@t.com", product_type="P", loan_amount=1000, interest_rate=5, tenure=12, emi=100)
    
    context = {
        'lead': lead,
        'emi': 100,
        'principal': 1000,
        'interest': 50,
        'principal_percent': 90,
        'interest_percent': 10,
    }
    html_string = render_to_string('pdf/loan_quotation.html', context)
    
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)
    if pdf.err:
        print("PDF ERROR:", pdf.err)
    else:
        print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
