from django.shortcuts import render
from rest_framework.views import APIView
from sslcommerz_lib import SSLCOMMERZ 
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from orders.models import Order
# Create your views here.
import os
import environ

env = environ.Env()
environ.Env.read_env()
STORE_ID= env('STORE_ID')
STORE_PASS= env('STORE_PASSWORD')

def generate_unique_trans_id():

    unique_code = uuid.uuid4().hex.upper()[:12]
    return f"TRAN-{unique_code}"




class PaymentView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self, request):
        trans_id=generate_unique_trans_id()
        data = request.data
        order_id = data['orderId']
        order =  Order.objects.get(id=order_id)
        order.status = "shipped"
        order.save()

            
        settings = { 'store_id': STORE_ID, 'store_pass': STORE_PASS, 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = data['totalPrice']
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trans_id
        post_body['success_url'] = f"https://eco-greens-client.vercel.app/payment/success/{trans_id}"
        post_body['fail_url'] = "https://eco-greens-client.vercel.app/payment/failed"
        post_body['cancel_url'] = "https://eco-greens-client.vercel.app/payment/failed"
        post_body['emi_option'] = 0
        post_body['cus_name'] = request.user.username
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] = data['phone']
        post_body['cus_add1'] = data['address']
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcz.createSession(post_body) # API response
        return Response({
            "message":"payment sucess",
            "data":response,
            'transId':trans_id
                     }) 
    # Need to redirect user to response['GatewayPageURL']





# @csrf_exempt
# def paymentSucess(request, trans_id: str):
#     return redirect(f"https://eco-greens-client.vercel.app/payment/success/{trans_id}")

@csrf_exempt
async def paymentSucess(request, trans_id: str):
    if request.method == 'GET':
        return render(request, 'payment_success.html', {'trans_id': trans_id})
    else:
        return Response({"error": "Method Not Allowed"}, status=405)



@csrf_exempt
async def paymentfailed(request):
    return redirect("https://eco-greens-client.vercel.app/payment/failed")