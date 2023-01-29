from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Tokens


def get_full_url(url: str) -> str:
    """
    Достаем полную ссылку по short_url
    Если ссылки нет в базе или она не активна
    возвращаем ошибку.
    Если все ок, то добавляем к счетчику статистики 1
    и возвращаем полную ссылку.
    """
    try:
        token = Tokens.objects.get(short_url__exact=url)
        if not token.is_active:
            raise KeyError('Token is no longer available')
    except Tokens.DoesNotExist:
        raise KeyError('Try another url. No such urls in DB')
    token.requests_count += 1
    token.save()
    return token.full_url


def redirection(request, short_url):
    """Перенаправляем кользователя по ссылке"""
    try:
        full_link = get_full_url(short_url)
        return redirect(full_link)
    except Exception as e:
        return HttpResponse(e.args)
