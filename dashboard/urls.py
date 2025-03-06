from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import SellerOrderAPIView, RevenueOverTimeAPIView,SellerOrderCountAPIView,TotalProductCountAPIView,UserOrderDataView,UserOrderCountAPIView
urlpatterns = [
    path('seller/orders/', SellerOrderAPIView.as_view(), name='seller-orders'),
    path('seller/order-count/', SellerOrderCountAPIView.as_view(), name='seller-order-count'),
    path('seller/total-product-count/',TotalProductCountAPIView.as_view(), name='seller-total-product-count'),
    path('seller/revenue/', RevenueOverTimeAPIView.as_view(), name='seller-revenue'),
    path('user/order-count/', UserOrderCountAPIView.as_view(),name='user-order-count'),
    path('user/order-data/',UserOrderDataView.as_view(),name='user-order-data'),
]
