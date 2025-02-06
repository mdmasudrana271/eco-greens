from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from . import serializers
from . import models
from django.template.loader import render_to_string


# for authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

# Create your views here.



class OrdersViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        order_items_data = request.data.get("order_items")  
        address = request.data.get("address")
        phone = request.data.get("phone")

        if not order_items_data:
            return Response({"error": "No plants provided for the order"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        order = models.Order.objects.create(user=user, address=address, phone=phone)

        email_data = []  # For sending order confirmation email

        for item in order_items_data:
            serializer = serializers.OrderItemSerializer(data=item)
            if serializer.is_valid():
                plant = serializer.validated_data['plant']
                quantity = serializer.validated_data['quantity']

                # Check if stock is available
                if quantity > plant.stock:
                    order.delete()  # Rollback if any item fails
                    return Response(
                        {"error": f"Only {plant.stock} items available for {plant.name}."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Calculate price and deduct stock
                price = plant.price * quantity
                total_price += price
                plant.stock -= quantity
                plant.save()

                # Create OrderItem
                models.OrderItem.objects.create(order=order, plant=plant, quantity=quantity, price=price)

                # Prepare email data
                email_data.append({
                    'id': order.id,
                    'order_date': order.order_date.strftime('%Y-%m-%d'),
                    'name': plant.name,
                    'price': float(plant.price),
                    'quantity': quantity,
                    'total': price
                })
            else:
                order.delete()  # Rollback order if any item fails
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update order total price
        order.total_price = total_price
        order.save()

        # Send order confirmation email
        self.send_order_email(user.email, email_data, total_price)

        return Response({'message':'Order Place Successfully', 'data':serializers.OrderSerializer(order).data, 'status':'success'})

    def send_order_email(self, to_email, email_data, total):
        """
        Sends an order confirmation email to the user.
        """
        subject = "Your Order Confirmation - GreenPlant Store"
        email_body = render_to_string('order_email.html', {'order': email_data, 'total': total})
        
        email = EmailMultiAlternatives(subject, '', to=[to_email])
        email.attach_alternative(email_body, "text/html")
        email.send()




class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):       
        # Get orders only for the authenticated user
        user_orders = models.Order.objects.filter(user=request.user).order_by('-order_date')
        
        # Serialize the orders
        serializer = serializers.OrderSerializer(user_orders, many=True)
        
        return Response({
            'data': serializer.data,
            'message': 'User Order History Retrieved Successfully'
        })





              