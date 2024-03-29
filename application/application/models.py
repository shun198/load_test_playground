from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """システムユーザ"""

    username_validator = UnicodeUsernameValidator()

    # 不要なフィールドはNoneにすることができる
    first_name = None
    last_name = None
    date_joined = None
    id = models.AutoField(
        primary_key=True,
        db_comment="ID",
    )
    employee_number = models.CharField(
        unique=True,
        validators=[RegexValidator(r"^[0-9]{8}$")],
        max_length=8,
        # 管理者のログイン画面で社員番号と表示される
        verbose_name="社員番号",
        db_comment="社員番号",
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        db_comment="ユーザ名",
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_comment="メールアドレス",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="更新日",
    )
    groups = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name="users",
        db_comment="社員権限テーブル外部キー",
    )

    USERNAME_FIELD = "employee_number"
    REQUIRED_FIELDS = ["email", "username"]

    class Meta:
        ordering = ["employee_number"]
        db_table = "User"
        db_table_comment = "システムユーザ"

    def __str__(self):
        return self.username


from application.utils.customer_storage import CustomerStorage


class Customer(models.Model):
    """お客様"""

    id = models.AutoField(
        primary_key=True,
        db_comment="ID",
    )
    kana = models.CharField(
        max_length=255,
        db_comment="カナ氏名",
    )
    name = models.CharField(
        max_length=255,
        db_comment="氏名",
    )
    birthday = models.DateField(
        db_comment="誕生日",
    )
    phone_no = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^[0-9]{11}$", "11桁の数字を入力してください。")],
        blank=True,
        db_comment="電話番号",
    )

    class Meta:
        db_table = "Customer"
        db_table_comment = "お客様"


class CustomerPhoto(models.Model):
    """お客様の画像"""

    id = models.AutoField(
        primary_key=True,
        db_comment="ID",
    )
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        db_comment="お客様ID",
    )
    photo = models.ImageField(
        upload_to="customer_photo",
        storage=CustomerStorage(),
        db_comment="写真",
    )

    class Meta:
        db_table = "CustomerPhoto"
        db_table_comment = "お客様の画像"
