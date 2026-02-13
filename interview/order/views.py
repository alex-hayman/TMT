from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrdersByDateRangeView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        embargo_date = request.query_params.get("embargo_date")

        if not start_date or not embargo_date:
            return Response(
                {"error": "Both start_date and embargo_date query parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        orders = Order.objects.filter(
            start_date__gte=start_date,
            embargo_date__lte=embargo_date
        )
        return Response(OrderSerializer(orders, many=True).data)
