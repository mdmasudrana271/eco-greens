from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
# Create your views here.



class PlantsViewset(viewsets.ModelViewSet):
    queryset = models.Plants.objects.all()
    serializer_class = serializers.PlantSerializer


class PlantsByCategory(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        # plants = models.Plants.objects.filter(category=category)
        # serializer = serializers.PlantSerializer(plants, many=True)
        # return Response({"data": serializer.data})

        if category:
            try:
                plants = models.Plants.objects.filter(category=category)
            except models.Plants.DoesNotExist:
                return Response({'message':"Category Not Found"})
        else:
            plants=models.Plants.objects.all()
        serializer=serializers.PlantSerializer(plants, many=True)
        return Response({'data':serializer.data,'message':'All Product'}) 


class PlantDetail(APIView):
    def get(self, request, id):
        try:
            plant = models.Plants.objects.get(id=id)
            serializer = serializers.PlantSerializer(plant)
            return Response({"data": serializer.data})
        except models.Plants.DoesNotExist:
            return Response({"error": "Plant not found."})
    
    def put(self, request, id):
        try:
            plant = models.Plants.objects.get(id=id)
            serializer = serializers.PlantSerializer(plant, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Plant updated successfully.", "data": serializer.data})
            return Response({"error": serializer.errors})
        except models.Plants.DoesNotExist:
            return Response({"error": "Plant not found."})
    
    def delete(self, request, id):
        try:
            plant = models.Plants.objects.get(id=id)
            plant.delete()
            return Response({"message": "Plant deleted successfully."})
        except models.Plants.DoesNotExist:
            return Response({"error": "Plant not found."})



class AddPlantsView(APIView):
    def post(self, request):
        serializer = serializers.PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Plant added successfully.", "data": serializer.data})
        return Response({"error": serializer.errors})