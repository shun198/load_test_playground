from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from application.serializers.user import LoginSerializer
from application.utils.get_client_ip import get_client_ip


class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """ログインAPI

        Args:
            request : リクエスト

        Returns:
            JsonResponse
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee_number = serializer.validated_data.get("employee_number")
        password = serializer.validated_data.get("password")
        user = authenticate(employee_number=employee_number, password=password)
        if not user:
            return JsonResponse(
                data={
                    "msg": "either employee number or password is incorrect"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            return JsonResponse(
                {
                    "username": user.username,
                    "role": user.groups.name,
                }
            )

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """ログアウトAPI

        Args:
            request : リクエスト

        Returns:
            HttpResponse
        """
        self.application_logger.info(
            f"ログアウト: {request.user}, IP: {get_client_ip(request)}"
        )
        logout(request)
        return HttpResponse()
