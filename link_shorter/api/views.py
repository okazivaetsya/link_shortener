from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenSerializer


class TokenAPIView(APIView):
    """Вьюха для работы с токенами"""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token, status_code = serializer.create(
                validated_data=serializer.validated_data
            )
            return Response(TokenSerializer(token).data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
