from django.contrib import admin
from .models import LoanQuotationLead, CalculatorAnalytics, UIInteractionLog, ContactUsLead, NewsletterSubscriber

@admin.register(LoanQuotationLead)
class LoanQuotationLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'product_type', 'loan_amount', 'interest_rate', 'tenure', 'emi', 'created_at')
    list_filter = ('product_type', 'created_at')
    search_fields = ('name', 'mobile', 'email')
    readonly_fields = ('created_at',)

@admin.register(CalculatorAnalytics)
class CalculatorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'created_at', 'metadata')
    list_filter = ('event_type', 'created_at')
    readonly_fields = ('created_at',)
