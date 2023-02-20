from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class MainViewTest(TestCase):

    def test_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertTemplateUsed(response, 'main/includes/header_actions.html')
        self.assertTemplateUsed(response, 'main/includes/minicart.html')
        self.assertTemplateUsed(response, 'main/includes/miniproduct.html')
        
        
