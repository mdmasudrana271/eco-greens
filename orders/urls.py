from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


router.register('list', views.OrdersViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('place_order/', views.PlaceOrderView.as_view(),name='place_order'),
    path('all_orders/', views.OrderListView.as_view(),name='all_orders'),
]