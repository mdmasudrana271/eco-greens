from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


# router.register('list', views.PlantsViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('pay/', views.PaymentView.as_view(),name='payment'),
    path('payment/success/<str:trans_id>/', views.paymentSucess, name='payment-success'),
    path('payment/failed/', views.paymentfailed, name='payment-failed'),
]