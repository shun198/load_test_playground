from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from application.models.user import User


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def add_arguments(self, parser):
        """システムユーザの数を指定するオプション

        Args:
            parser : オプションを追加するためのparser
        """
        parser.add_argument(
            "--users",
            type=int,
            help="Specify the amount of users. The default amount of users will be 10",
        )

    def handle(self, *args, **options):
        """システムユーザを作成するコマンド"""
        Group.objects.update_or_create(
            id=1,
            name="管理者",
        )
        Group.objects.update_or_create(
            id=2,
            name="一般",
        )
        users = options["users"]
        if not users:
            users = 10
        print(f"Creating {users} users")
        for id in range(1, users + 1):
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    id=id,
                    username=f"テストユーザ{id}",
                    employee_number=str(id).zfill(8),
                    email=f"example{id}.com",
                    groups=Group.objects.get(name="管理者"),
                )
            user.set_password("test")
            user.save()
            print(f"Created {user}")
        print(f"Successfully created {users} users")
