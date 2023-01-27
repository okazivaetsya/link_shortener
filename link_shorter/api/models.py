import random
from django.conf import settings
from django.db import models


class Tokens(models.Model):
    full_url = models.URLField(unique=True)
    short_url = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True
    )
    requests_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    def save(self, *args, **kwargs):
        """
        При создании токена,
        короткая ссылка генерится автоматически
        """
        if not self.short_url:
            self.short_url = ''.join(
                random.choices(
                    settings.CHARACTERS,
                    k=settings.TOKEN_LENGTH
                )
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.short_url} -> {self.full_url}'
