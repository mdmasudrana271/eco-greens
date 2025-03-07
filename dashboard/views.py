from rest_framework.response import Response
from orders.models import Order, OrderItem, Plants
from orders.serializers import OrderSerializer
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum

# for authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SellerOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        seller = request.user.userprofile
        seller_plants = Plants.objects.filter(seller=seller)
        order_ids = OrderItem.objects.filter(plant__in=seller_plants).values_list('order', flat=True)
        # orders = Order.objects.filter(id__in=order_ids)
        orders = Order.objects.filter(id__in=order_ids,status='pending').order_by('-order_date')

  
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    




class SellerOrderCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        seller = request.user.userprofile
        orders = Order.objects.filter(order_items__plant__seller=seller)
        seller_plants = Plants.objects.filter(seller=seller)
        total_plants = seller_plants.count()
        total_orders = orders.count()

        
        # revenue = orders.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
        revenue = orders.filter(status='shipped').aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0

        return Response({
            'total_products': total_plants,
            'total_orders': total_orders,
            'revenue': revenue,
        })


class TotalProductCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        seller = request.user.userprofile
        seller_plants = Plants.objects.filter(seller=seller)
        total_products = seller_plants.count()
        return Response({'total_products': total_products})


class RevenueOverTimeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        seller = request.user.userprofile
        # orders = Order.objects.filter(order_items__plant__seller=seller)
        orders = Order.objects.filter(
            order_items__plant__seller=seller, 
            status='shipped'  # Filter by order status
        )
        monthly_revenue = {}

        for order in orders:
            month = order.order_date.strftime('%b %Y')
            monthly_revenue[month] = monthly_revenue.get(month, 0) + order.total_price

        sorted_months = sorted(monthly_revenue.keys())
        revenue_values = [monthly_revenue[month] for month in sorted_months]

        return Response({
            'labels': sorted_months,
            'datasets': [{
                'label': 'Revenue',
                'data': revenue_values,
                'borderColor': '#4CAF50',
                'backgroundColor': 'rgba(76, 175, 80, 0.2)',
                'fill': True
            }]
        })
    



class UserOrderDataView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        orders = (
            Order.objects.filter(user=user)
            .annotate(month=TruncMonth('order_date'))
            .values('month')
            .annotate(order_count=Count('id'))
            .order_by('month')
        )

        labels = [order['month'].strftime('%b %Y') for order in orders]
        datasets = [{'data': [order['order_count'] for order in orders]}]

        return Response({
            'labels': labels,
            'datasets': datasets,
        })


class UserOrderCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        total_orders = Order.objects.filter(user=user).count()
        total_cost = Order.objects.filter(user=user).aggregate(Sum('total_price'))['total_price__sum'] or 0

        return Response({
            'total_orders': total_orders,
            'total_cost': total_cost,
        })
    

