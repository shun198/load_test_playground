import csv
import io

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Customer
from application.serializers.customer import (
    CreateCustomerSerializer,
    CustomerSerializer,
)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomerFilter

    def get_serializer_class(self):
        if self.action == "import_customer_csv":
            return CreateCustomerSerializer
        else:
            CustomerSerializer

    @action(detail=False, methods=["POST"])
    def import_customer_csv(self, request, *args, **kwargs):
        csv_file = request.FILES["file"]
        # utf-8に変換
        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        # header(1行目)を無視
        header = next(csv.reader(io_string))
        for row in csv.reader(io_string, delimiter=","):
            csv_data = {
                "kana": row[0],
                "name": row[1],
                "birthday": row[2],
                "phone_no": row[3],
            }
            serializer = CustomerSerializer(data=csv_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return JsonResponse(
            {"msg": "CSVファイルのアップロードに成功しました"},
            status=status.HTTP_201_CREATED,
        )
