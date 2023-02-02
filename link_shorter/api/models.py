import random

from django.conf import settings
from django.db import models


class Tokens(models.Model):
    """
    Модель ТОКЕН
    Токеном в данном случае называется пара (short_url -> full_url)

    Поле is_active (активен ли токен) по умолчанию True,
    никаких указаний на это счет в ТЗ не было,
    поэтому я его добавил на перспективу,
    чтобы можно было включать/выключать те или иные токены.
    """
    full_url = models.URLField(unique=True)
    short_url = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True
    )
    requests_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date',)

    def save(self, *args, **kwargs):
        """
        При создании токена достаточно только полной ссылки,
        короткая ссылка генерится автоматически.
        Перед сохранением объекта токен проверятеся на уникальность
        """
        if not self.short_url:
            while True:
                self.short_url = ''.join(
                    random.choices(
                        settings.CHARACTERS,
                        k=settings.TOKEN_LENGTH
                    )
                )
                if not Tokens.objects.filter(
                    short_url=self.short_url
                ).exists():
                    break
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.short_url} -> {self.full_url}'
