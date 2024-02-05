from rest_framework import serializers

from application.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


# ファイルアップロード用Serializer
class CreateCustomerSerializer(serializers.Serializer):
    file = serializers.FileField()
