from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


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
        self._create_or_update_group()
        users = options["users"]
        if not users:
            users = 10
        for i in range(1, users + 1):
            print(f"{i}:作成開始")

    def _create_or_update_group(self):
        """システムユーザの権限グループを作成または更新するメソッド"""
        Group.objects.update_or_create(
            id=1,
            name="管理者",
        )
        Group.objects.update_or_create(
            id=2,
            name="一般",
        )
