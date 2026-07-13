from django.contrib import admin

from .models import (
    LoanQuotationLead,
    CalculatorAnalytics,
    UIInteractionLog,
    NewsletterSubscriber,
    EnquiryLead,
    ConsultationLead,
)


# ==========================================================
# Loan Quotation Leads
# ==========================================================

@admin.register(LoanQuotationLead)
class LoanQuotationLeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mobile',
        'email',
        'product_type',
        'loan_amount',
        'interest_rate',
        'tenure',
        'emi',
        'created_at',
    )

    list_filter = (
        'product_type',
        'created_at',
    )

    search_fields = (
        'name',
        'mobile',
        'email',
    )

    readonly_fields = (
        'created_at',
    )




# ==========================================================
# Newsletter
# ==========================================================

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "is_active",
        "subscribed_at",
    )

    search_fields = (
        "email",
    )

    list_filter = (
        "is_active",
        "subscribed_at",
    )

    readonly_fields = (
        "subscribed_at",
    )


# ==========================================================
# Guide Enquiry Leads
# ==========================================================

@admin.register(EnquiryLead)
class EnquiryLeadAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# Consultation Leads
# ==========================================================

@admin.register(ConsultationLead)
class ConsultationLeadAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "financial_segment",
        "monthly_salary",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    list_filter = (
        "financial_segment",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# Calculator Analytics
# ==========================================================

@admin.register(CalculatorAnalytics)
class CalculatorAnalyticsAdmin(admin.ModelAdmin):

    list_display = (
        'event_type',
        'created_at',
    )

    list_filter = (
        'event_type',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )


# ==========================================================
# UI Interaction Logs
# ==========================================================

@admin.register(UIInteractionLog)
class UIInteractionLogAdmin(admin.ModelAdmin):

    list_display = (
        "event_type",
        "element_id",
        "page_url",
        "created_at",
    )

    search_fields = (
        "event_type",
        "element_id",
        "page_url",
    )

    list_filter = (
        "event_type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )