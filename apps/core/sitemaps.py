from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "core:home",
            "core:personal_loan",
            "core:mortgage",
            "core:credit_card",
            "core:business_loan",
            "core:business_account",
            "core:about_us",
            "core:become_partner",
            "core:contact_us",
            "core:faq",
            "core:our_leaders",
            "core:bdp_guides",
            "core:bdp_faq",
        ]

    def location(self, item):
        return reverse(item)