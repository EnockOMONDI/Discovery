from django.test import TestCase
from django.urls import reverse
from .models import DiscoveryResponse


def valid_payload(**overrides):
    data = {
        "company_name": "Sample Travel",
        "contact_person": "Jane Example",
        "email": "jane@example.test",
        "main_services": "Safaris, beach holidays and corporate retreats.",
        "booking_workflow": "Client asks on WhatsApp, team quotes, then follows up payment.",
        "urgent_priorities": "Clean up packages and make follow-up easier.",
        "success_30_60_90": "More inquiries, consistent content and better reporting.",
        "ownership_scope": "Creative, website updates and reporting.",
        "priority_offers": ["safaris", "beach_holidays"],
        "consent": "yes",
    }
    data.update(overrides)
    return data


class DiscoveryFormTests(TestCase):
    def test_form_loads(self):
        response = self.client.get(reverse("discovery_form"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Travel Business Discovery")
        self.assertContains(response, "Step 1 of 7")

    def test_valid_submission_saves_response(self):
        response = self.client.post(reverse("discovery_form"), valid_payload())
        self.assertEqual(response.status_code, 302)
        saved = DiscoveryResponse.objects.get()
        self.assertEqual(saved.company_name, "Sample Travel")
        self.assertEqual(saved.answers["priority_offers"], ["safaris", "beach_holidays"])
        self.assertTrue(saved.consent)

    def test_required_fields_are_validated(self):
        response = self.client.post(reverse("discovery_form"), valid_payload(company_name="", consent=""))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please answer this before submitting.")
        self.assertContains(response, "Please confirm that these answers can be stored")
        self.assertFalse(DiscoveryResponse.objects.exists())

    def test_honeypot_blocks_submission(self):
        response = self.client.post(reverse("discovery_form"), valid_payload(company_site="spam"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DiscoveryResponse.objects.exists())
