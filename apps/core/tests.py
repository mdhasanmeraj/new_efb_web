from django.test import TestCase
from django.urls import reverse

class TermsAndConditionsTests(TestCase):
    def test_terms_page_status_code(self):
        url = reverse('core:terms_and_conditions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/terms_and_conditions.html')
        self.assertContains(response, "Terms & Conditions")

    def test_privacy_cookies_policy_page(self):
        url = reverse('core:privacy_cookies_policy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/privacy_cookies_policy.html')
        self.assertContains(response, "Privacy & Cookies Policy")

    def test_disclaimer_page(self):
        url = reverse('core:disclaimer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/disclaimer.html')
        self.assertContains(response, "Disclaimer")

    def test_bdp_terms_and_conditions_page(self):
        url = reverse('core:bdp_terms_and_conditions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/bdp_terms_and_conditions.html')
        self.assertContains(response, "BDP Terms & Conditions")

    def test_bdp_privacy_policy_page(self):
        url = reverse('core:bdp_privacy_policy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/bdp_privacy_policy.html')
        self.assertContains(response, "BDP Privacy Policy")

    def test_terms_pdf_download_status_code(self):
        url = reverse('core:download_guide', kwargs={'filename': 'Terms_and_Conditions_EFB.pdf'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_privacy_cookies_pdf_download(self):
        url = reverse('core:download_guide', kwargs={'filename': 'Privacy_&_Cookies_Policy.pdf'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_disclaimer_pdf_download(self):
        url = reverse('core:download_guide', kwargs={'filename': 'Disclaimer_EFB.pdf'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_bdp_terms_pdf_download(self):
        url = reverse('core:download_guide', kwargs={'filename': 'EFB_BDP_Terms_and_Conditions.pdf'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_bdp_privacy_pdf_download(self):
        url = reverse('core:download_guide', kwargs={'filename': 'BDP_Privacy_Policy.pdf'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
