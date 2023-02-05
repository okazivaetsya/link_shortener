from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Tokens


class TestAPI(APITestCase):
    """Тестируем POST запросы"""
    url = '/api/tokens/'

    def setUp(self) -> None:
        Tokens.objects.create(
            full_url='https://ya.ru/',
            short_url='aEdj01',
        )

    def test_token_get(self):
        """Проверка получения уже существующего токена"""
        existing_data = {
            'full_url': 'https://ya.ru/'
        }
        response_get = self.client.post(self.url, data=existing_data)
        result_get = response_get.json()

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(Tokens.objects.all().count(), 1)
        self.assertEqual(result_get['full_url'], 'https://ya.ru/')
        self.assertEqual(result_get['short_url'], 'aEdj01')
        self.assertIsInstance(result_get, dict)
        self.assertEqual(len(result_get), 6)

    def test_token_create(self):
        """
        Проверка создания токена без явного указания короткой ссылки
        и с явным указанием короткой ссылки
        """
        creation_data = {
            'full_url': 'http://post.url.test.ru'
        }
        creation_full_data = {
            'full_url': 'http://test.ru',
            'short_url': 'Q2We34'
        }
        response_create = self.client.post(self.url, data=creation_data)
        result_create = response_create.json()

        response_create_with_short_url = self.client.post(
            self.url, data=creation_full_data
        )
        result_create_with_short_url = response_create_with_short_url.json()

        self.assertEqual(response_create.status_code, 201)
        self.assertEqual(result_create['full_url'], 'http://post.url.test.ru')
        self.assertEqual(len(result_create['short_url']), 6)
        self.assertIsInstance(result_create, dict)
        self.assertEqual(Tokens.objects.all().count(), 3)
        self.assertEqual(len(result_create), 6)
        self.assertEqual(
            result_create_with_short_url['full_url'],
            'http://test.ru',
            msg='Ошибка full_url'
        )
        self.assertEqual(
            result_create_with_short_url['short_url'],
            'Q2We34',
            msg='Ошибка short_url'
        )


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
        """Тестируем переадресацию"""
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
