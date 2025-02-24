from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

# Create your views here.



class UserProfilesViewset(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("token ", token)
            # models.Donor.objects.create(user=user)
            print("uid ", uid)
            confirm_link = f"https://eco-greens.vercel.app/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({'data':"Check your mail for confirmation"})
        return Response(serializer.errors)
    


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://eco-greens-client.vercel.app/login')
    else:
        return redirect('https://eco-greens-client.vercel.app/signup')
    




class UserLoginApiView(APIView):
    def post(self,request):
        serializer=serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']

            user=authenticate(username=username,password=password)

            if user:
                token,_=Token.objects.get_or_create(user=user)
                login(request,user)
                return Response(
                    {
                    'token':token.key,
                    'user_id':user.id,
                    'username':username,
                    'account_type':user.userprofile.account_type
                   
                })
            else:

                return Response({'error':'Invalid Credintial'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)
    



class UserDetailsView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self,request, user_id):
    
        try:
            
            profiles = models.UserProfile.objects.get(user_id=user_id)
            
            user = {
                'id': profiles.user.id,
                'username':profiles.user.username,
                'first_name': profiles.user.first_name,
                'last_name': profiles.user.last_name,
                'email': profiles.user.email,
                'account_type': profiles.account_type,
                'mobile_no': profiles.mobile_no,
                'address': profiles.address,
            }
            
            return Response({'status': 'success','data': user})
    
        except models.UserProfile.DoesNotExist:
        
            return Response({'status': 'error','message': 'User profile not found'} , status=status.HTTP_404_NOT_FOUND)
     




class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = serializers.UpdateUserProfileSerializer(user,
            data=request.data, 
            partial=True,  # Allows updating only specific fields
            context={'request': request}
        )

        if serializer.is_valid():
            # Update User fields
            user.email = serializer.validated_data.get('email', user.email)
            user.first_name = serializer.validated_data.get('first_name', user.first_name)
            user.last_name = serializer.validated_data.get('last_name', user.last_name)

            # Update UserProfile fields
            profile = user.userprofile
            profile.mobile_no = serializer.validated_data.get('mobile_no', profile.mobile_no)
            profile.address = serializer.validated_data.get('address', profile.address)

            user.save()
            profile.save()

            return Response({
                "message": "User updated successfully.",
                'data': serializer.data
            }, status=200)
        else:
            return Response(serializer.errors, status=400)





class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message": "Logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)