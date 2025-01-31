from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from . serializers import CategorySerializer
from . import models
from userprofile.permissions import IsSeller
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = models.Categories.objects.all()
    serializer_class = CategorySerializer


class CreateCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsSeller]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category created successfully.", "data": serializer.data})
        return Response({"error":serializer.errors})
    


class CategoryDetail(APIView):
    def get(self, request, id):
        try:
            category = models.Categories.objects.get(id=id)
            serializer = CategorySerializer(category)
            return Response({"data": serializer.data})
        except models.CategoriesModel.DoesNotExist:
            return Response({"error": "Category not found."})