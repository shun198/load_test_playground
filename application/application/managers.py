from django.contrib.auth.models import BaseUserManager, Group
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """社員を作成する為のクラス"""

    use_in_migrations = True

    def create_or_update_user(
        self,
        id: int,
        username: str,
        employee_number: str,
        email: str,
        groups: Group,
        **extra_fields,
    ):
        """社員を作成または更新

        Args:
            username (str): 社員氏名
            employee_number (str): 社員番号
            email (str): Eメール
            group (Group): 社員権限
        Returns:
            作成した社員
        """
        try:
            groups, _ = Group.objects.get(name=groups.value)
        except:
            groups = 1
        try:
            user = self.model.get(id=id)
            user.username = getattr(user,"username",f"テストユーザ{id}")
            user.employee_number = getattr(user,"employee_number",f"テストユーザ{id}")
            user.email = getattr(user,"email",f"example{id}.com")
            user.groups = groups
        except:
            user = self.model(
                username=getattr(user,"username",f"テストユーザ{id}"),
                employee_number=getattr(user,"employee_number",f"テストユーザ{id}"),
                email=getattr(user,"email",f"example{id}.com"),
                groups=groups,
                **extra_fields,
            )
        user.set_password("test")
        user.save(using=self._db)

        return user
