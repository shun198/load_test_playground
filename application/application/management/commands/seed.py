from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        parser.add_argument(
            "--users",
            type=int,
            help="Specify the amount of users",
        )

    def handle(self, *args, **options):
        users = options["users"]
        if users:
            print(users)
        print("no users")
