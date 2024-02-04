from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.emails import send_welcome_email
from application.models.user import User
from application.permissions import IsAdminUser, IsSuperUser
from application.serializers.user import EmailSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "send_invite_user_mail":
            return EmailSerializer
        elif self.action == "create_user":
            return None
        else:
            return UserSerializer

    @action(detail=False, methods=["POST"])
    def send_invite_user_mail(self, request):
        """指定したメールアドレス宛へ招待メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        serializer = self.get_serializer(data=request.data)
        # バリデーションに失敗したら400を返す
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        email = serializer.validated_data.get("email")
        # メール送信用メソッド
        send_welcome_email(email=email)
        return HttpResponse()

    @action(detail=False, methods=["POST"])
    def create_user(self, request):
        """指定したメールアドレス宛へ招待メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        User.objects.create_or_update_user(id=10)
        return HttpResponse()

    # get_permissionsメソッドを使えば前述の表に従って権限を付与できる
    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "send_invite_user_mail",
        ]:
            permission_classes = [IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        elif self.action == "create_user":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
