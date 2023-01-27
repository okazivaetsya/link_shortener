from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenSerializer


class TokenAPIView(APIView):
    """Вьюха для работы с токенами"""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, 201)
