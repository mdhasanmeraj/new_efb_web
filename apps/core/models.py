from django.db import models

class LoanQuotationLead(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    product_type = models.CharField(max_length=50)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure = models.IntegerField(help_text="Tenure in months")
    emi = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product_type} - AED {self.loan_amount}"


class CalculatorAnalytics(models.Model):
    EVENT_CHOICES = [
        ('Calculator Opened', 'Calculator Opened'),
        ('EMI Calculated', 'EMI Calculated'),
        ('Quote Downloaded', 'Quote Downloaded'),
    ]
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True, help_text="Additional event context like loan_amount, tenure, rate, user_agent, etc.")

    def __str__(self):
        return f"{self.event_type} at {self.created_at}"


class UIInteractionLog(models.Model):
    user_session_id = models.CharField(max_length=255, db_index=True)
    element_id = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=100)
    page_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_type} on {self.page_url} by {self.user_session_id}"





class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# ==========================================================
# BDP Guide Enquiry Lead
# ==========================================================

class EnquiryLead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Enquiry Lead"
        verbose_name_plural = "Enquiry Leads"

    def __str__(self):
        return f"{self.name} ({self.email})"


# ==========================================================
# Free Consultation Lead
# ==========================================================

class ConsultationLead(models.Model):
    FINANCIAL_SEGMENTS = [
    ("Personal Loan", "Personal Loan"),
    ("Business Loan", "Business Loan"),
    ("Business Account", "Business Account"),
    ("Mortgage", "Mortgage"),
    ("Credit Card", "Credit Card"),
]

    name = models.CharField(max_length=255)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    financial_segment = models.CharField(
        max_length=100,
        choices=FINANCIAL_SEGMENTS
    )

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Consultation Lead"
        verbose_name_plural = "Consultation Leads"

    def __str__(self):
        return f"{self.name} - {self.financial_segment}"