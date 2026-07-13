import re
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    LoanQuotationLead,
    NewsletterSubscriber,
    EnquiryLead,
    ConsultationLead,
)

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


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']


# ==========================================================
# BDP Guide Enquiry Form
# ==========================================================

class EnquiryLeadForm(forms.ModelForm):

    class Meta:
        model = EnquiryLead
        fields = [
            "name",
            "email",
            "message",
        ]


# ==========================================================
# Consultation Form
# ==========================================================

class ConsultationLeadForm(forms.ModelForm):

    class Meta:
        model = ConsultationLead

        fields = [
            "name",
            "email",
            "phone",
            "financial_segment",
            "monthly_salary",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        pattern = r'^(\+9715\d{8}|05\d{8})$'

        if not re.match(pattern, phone):
            raise ValidationError(
                "Please enter a valid UAE mobile number."
            )

        return phone