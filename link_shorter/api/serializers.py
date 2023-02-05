from rest_framework import serializers, status

from .models import Tokens


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки запросов на создание токенов:

    В сериализаторе убрана валидация full_url,
    но она осталась на уровне модели.
    Это сделано для того чтобы is_valid пропускал данные
    и можно было сериализовать их при уже существующем токене.
    """

    class Meta:
        model = Tokens
        fields = '__all__'
        extra_kwargs = {'full_url': {'validators': []}}

    def create(self, validated_data):
        """
        Переопределенный метод create:
        возвращает существующий токен
        или создает новый и возвращает его.
        """
        full_url = validated_data['full_url']
        try:
            short_url = validated_data['short_url']
            token, created = Tokens.objects.get_or_create(
                full_url=full_url, short_url=short_url
            )
        except KeyError:
            token, created = Tokens.objects.get_or_create(
                full_url=full_url
            )
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK
        return token, status_code
