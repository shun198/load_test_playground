from datetime import datetime, timedelta

import factory
from factory import Faker, Sequence, SubFactory

from application.models import Customer


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    kana = Sequence(lambda n: "テストコキャク{}".format(n))
    name = Sequence(lambda n: "テスト顧客{}".format(n))
    birthday = Faker(
        "date_between_dates",
        date_start=(datetime.now().date() - timedelta(days=365 * 50)),
        date_end=(datetime.now().date() - timedelta(days=365 * 20)),
    )
    phone_no = Sequence(lambda n: f"080" + "{0:08}".format(n + 100))

