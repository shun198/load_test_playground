from django.contrib.auth.models import BaseUserManager, Group


class UserManager(BaseUserManager):
    """社員を作成する為のクラス"""

    use_in_migrations = True

    def create_or_update_user(
        self,
        id: int,
        **extra_fields,
    ):
        """社員を作成または更新

        Args:
            id: 社員ID
        Returns:
            作成した社員
        """

        try:
            user = self.model.objects.get(id=id)
            user.username = extra_fields.setdefault("username", f"テストユーザ{id}")
            user.employee_number = (
                extra_fields.setdefault("employee_number", id),
            )
            user.email = (
                extra_fields.setdefault("email", f"example{id}.com"),
            )
            user.groups = Group.objects.get(
                name=extra_fields.setdefault("group", "管理者")
            )
        except self.model.DoesNotExist:
            user = self.model(
                id=id,
                username=extra_fields.setdefault("username", f"テストユーザ{id}"),
                employee_number=extra_fields.setdefault("employee_number", id),
                email=extra_fields.setdefault("email", f"example{id}.com"),
                groups=Group.objects.get(
                    name=extra_fields.setdefault("group", "管理者")
                ),
            )
        user.set_password("test")
        user.save(using=self._db)

        return user
