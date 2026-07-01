import re
from django import forms
from django.core.exceptions import ValidationError
from .models import LoanQuotationLead, ContactUsLead, NewsletterSubscriber

class LoanQuotationLeadForm(forms.ModelForm):
    class Meta:
        model = LoanQuotationLead
        fields = ['name', 'mobile', 'email', 'product_type', 'loan_amount', 'interest_rate', 'tenure', 'emi']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '').strip()
        # Accept +9715XXXXXXXX (971 + 5 + 8 digits) or 05XXXXXXXX (05 + 8 digits)
        pattern = r'^(\+9715\d{8}|05\d{8})$'
        if not re.match(pattern, mobile):
            raise ValidationError("Invalid UAE Mobile Number. Must be +971XXXXXXXXX or 05XXXXXXXX")
        return mobile

class ContactUsLeadForm(forms.ModelForm):
    class Meta:
        model = ContactUsLead
        fields = ['name', 'email', 'phone', 'message']

class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
