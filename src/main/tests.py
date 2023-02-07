import unittest

from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve, reverse
from main.views import MainView


class SmokeTest(TestCase):
    '''тест на токсичность'''
    def test_bad_maths(self):
        '''тест: неправильные математические расчеты'''
        self.assertEqual(1 + 1, 2)
        
        
class HomePageTest(TestCase):
    '''тест домашней страницы'''
    def test_root_url_resolves_to_home_page_view(self):
        '''тест: корневой url преобразуется в представление
        домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func.view_class, MainView)

    def some_test(self):
        client = Client()
        response = client.get(reverse('main:index'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница возвращает правильный html'''

        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.strip().startswith('<!doctype html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertTemplateUsed(response, 'main/includes/minicart.html')
        self.assertTemplateUsed(response, 'base.html')
        
        
class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()
    
        def tearDown(self):
            '''демонтаж'''
    
        self.browser.quit()