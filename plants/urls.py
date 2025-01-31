from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


router.register('list', views.PlantsViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('add/', views.AddPlantsView.as_view(),name='add_plants'),
    path('update/<int:id>/', views.PlantDetail.as_view(),name='update_plant'),
    path('all/', views.PlantsByCategory.as_view(),name='all_category'),
    path('details/<int:id>/', views.PlantDetail.as_view(),name='details'),
]