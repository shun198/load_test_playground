from django.contrib.auth.models import BaseUserManager, Group
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """社員を作成する為のクラス"""

    use_in_migrations = True

    def create_or_update_user(
        self,
        name: str,
        employee_number: str,
        email: str,
        group: Group,
        **extra_fields,
    ):
        """社員を作成または更新

        Args:
            name (str): 社員氏名
            employee_number (str): 社員番号
            email (str): Eメール
            group (Group): 社員権限
        Returns:
            作成した社員
        """

        group, _ = Group.objects.get_or_create(name=group.value)

        user = self.model(
            name=name,
            employee_number=employee_number,
            email=email,
            groups=group,
            **extra_fields,
        )

        user.set_password(get_random_string(16))
        user.save(using=self._db)

        return user
