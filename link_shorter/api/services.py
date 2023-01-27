from .models import Tokens
from django.http import HttpResponse
from django.shortcuts import redirect


def get_full_url(url: str) -> str:
    try:
        token = Tokens.objects.get(short_url__exact=url)
    except Tokens.DoesNotExist:
        raise KeyError("В базе нет такой ссылки")
    token.requests_count += 1
    token.save()
    return token.full_url


def redirection(request, short_url):
    try:
        full_link = get_full_url(short_url)
        return redirect(full_link)
    except Exception as e:
        return HttpResponse(e.args)
