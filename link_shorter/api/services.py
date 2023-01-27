from .models import Tokens
from django.http import HttpResponse
from django.shortcuts import redirect


def get_full_url(url: str) -> str:
    """
    Достаем полную ссылку по short_url
    Если ссылки нет в базе или она не активна
    возвращаем ошибку.
    Если все ок, то добавляем к счеткику перезодов 1
    и возвращаем полную ссылку.
    """
    try:
        token = Tokens.objects.get(short_url__exact=url)
        if not token.is_active:
            raise KeyError("Ссылка больше не доступна")
    except Tokens.DoesNotExist:
        raise KeyError("В базе нет такой ссылки")
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
