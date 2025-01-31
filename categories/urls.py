from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


router.register('list', views.CategoryViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateCategory.as_view(),name='create'),
    # path('update/<int:id>', UpdelCategory.as_view(),name='updatedel'),
    # path('all/', AllCategory.as_view(),name='all_category'),
    path('details/<int:id>/', views.CategoryDetail.as_view(),name='details'),
]