from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Tokens


class TestAPI(APITestCase):
    """Тестируем POST запросы"""
    url = '/api/tokens/'

    def test_token_creation(self):
        """Проверка создания токенра через api"""
        data = {
            'full_url': 'http://post.url.test.ru'
        }
        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['full_url'], 'http://post.url.test.ru')
        self.assertEqual(len(result['short_url']), 6)
        self.assertIsInstance(result, dict)
        self.assertEqual(Tokens.objects.all().count(), 1)


class TestRedirection(TestCase):
    """Тестируем GET запросы"""
    active_url = '/aEdj01'
    deactive_url = '/q2Nb23'

    def setUp(self) -> None:
        Tokens.objects.create(
            full_url='https://ya.ru/',
            short_url='aEdj01',
        )

        Tokens.objects.create(
            full_url='https://stackoverflow.com/',
            short_url='q2Nb23',
            is_active=False
        )

    def test_redirection(self):
        """Тестируем счетчик запросов токена"""
        response = self.client.get(self.active_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://ya.ru/')

    def test_response_counter(self):
        """Тестируем счетчик запросов токена"""
        self.assertEqual(
            Tokens.objects.get(short_url='aEdj01').requests_count, 0
        )
        self.client.get(self.active_url)
        self.assertEqual(
            Tokens.objects.get(short_url='aEdj01').requests_count, 1
        )
        self.assertEqual(
            Tokens.objects.get(short_url='q2Nb23').requests_count, 0
        )
        self.client.get(self.deactive_url)
        self.assertEqual(
            Tokens.objects.get(short_url='q2Nb23').requests_count, 0
        )

    def test_deactive_url(self):
        """Тестируем неактивные токены"""
        response = self.client.get(self.deactive_url)
        self.assertEqual(response.content, b'Token is no longer available')
