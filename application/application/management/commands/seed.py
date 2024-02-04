from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            help="Specify the amount of users. The default amount of users will be 10",
        )

    def handle(self, *args, **options):
        users = options["users"]
        if not users:
            print("no users")
            users = 10
            print(users)
