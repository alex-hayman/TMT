from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersByDateRangeView


urlpatterns = [
    path("tags/", OrderTagListCreateView.as_view(), name="order-detail"),
    path("by-date-range/", OrdersByDateRangeView.as_view(), name="orders-by-date-range"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
