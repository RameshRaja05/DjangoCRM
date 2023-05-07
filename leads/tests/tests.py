from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class LandingPageTest(TestCase):
    def test_get(self):
        res=self.client.get(reverse('landing-page'))
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,'landing-page.html')