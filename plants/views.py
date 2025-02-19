from django.shortcuts import render
from rest_framework import viewsets,pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.authentication import TokenAuthentication
from userprofile.permissions import  IsSeller
from rest_framework.permissions import IsAuthenticated
from .serializers import PlantSerializer
# Create your views here.




# pagination class 

class PlantsPagination(pagination.PageNumberPagination):
    page_size = 10 # items per page
    page_size_query_param = "page_size"
    max_page_size = 30



class PlantsViewset(viewsets.ModelViewSet):
    queryset = models.Plants.objects.all()
    serializer_class = serializers.PlantSerializer
    pagination_class = PlantsPagination


# class PlantsByCategory(APIView):
#     pagination_class = PlantsPagination
#     def get(self, request):
#         category = request.query_params.get('category', None)

#         if category:
#             try:
#                 plants = models.Plants.objects.filter(category=category)
#             except models.Plants.DoesNotExist:
#                 return Response({'message':"Category Not Found"})
#         else:
#             plants=models.Plants.objects.all()
#         serializer=serializers.PlantSerializer(plants, many=True)
#         return Response({'data':serializer.data,'message':'All Product'}) 



class PlantsByCategory(APIView):
    pagination_class = PlantsPagination  # Define pagination class

    def get(self, request):
        category = request.query_params.get('category', None)

        if category:
            plants = models.Plants.objects.filter(category=category)
        else:
            plants = models.Plants.objects.all()

        paginator = self.pagination_class()  # Create paginator instance
        paginated_queryset = paginator.paginate_queryset(plants, request)

        serializer = PlantSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response({
            'data': serializer.data,
            'message': 'All Products'
        })





class PlantDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
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
        




class PlantsBySeller(APIView):
    permission_classes = [IsSeller]
    authentication_classes = [TokenAuthentication]
    pagination_class = PlantsPagination
    def get(self, request):
        user = request.user
        account_type = user.userprofile.account_type

        if self.request.user.userprofile.account_type=='Seller':
            try:
                user_profile = models.UserProfile.objects.get(user__username=user.username)
                
                plants = models.Plants.objects.filter(seller=user_profile)
                serializer = serializers.PlantSerializer(plants, many=True)
                
                return Response({"data": serializer.data, "message": f"Plants added by {user.username}"})
            except models.UserProfile.DoesNotExist:
                return Response({"error": "Seller with this username does not exist."})
        else:
            return Response({"error": "Seller username is required."})




class AddPlantsView(APIView):
    permission_classes = [IsSeller]
    authentication_classes = [TokenAuthentication]
    # parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        print("Received data:", request.data)
        serializer = serializers.PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user.userprofile)
            return Response({"message": "Plant added successfully.", "data": serializer.data})
        return Response({"error": serializer.errors})
    



class BlogViewset(viewsets.ModelViewSet):
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, plant_id):
        if plant_id:
            blogs = models.Blog.objects.filter(plant__id=plant_id).order_by('-created_at')
        else:
            blogs = models.Blog.objects.all()

        serializer = serializers.BlogSerializer(blogs, many=True)
        return Response({"data": serializer.data})
    

    def post(self, request):
        print("Received data:", request.data)
        serializer = serializers.BlogSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save(author=request.user.userprofile)
            serializer.save(author=request.user.userprofile)  
            return Response({"message": "Blog added successfully.", "data": serializer.data})
        return Response({"error": serializer.errors})