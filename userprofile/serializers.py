from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from . constant import Account_type




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'read_only': True},  # Make username non-editable
        }

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = UserProfile
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    account_type=serializers.ChoiceField(choices=Account_type,default='Buyer',required=False)
    mobile_no=serializers.CharField(max_length=12)
    address=serializers.CharField(max_length=100,required=False)


    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password', 'confirm_password', 'account_type', 'mobile_no', 'address']
        # read_only_fields = ['account_type']


    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        mobile_no=self.validated_data['mobile_no']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']
        address = self.validated_data.get('address')
        account_type = self.validated_data.get('account_type')
       

        if password != confirm_password:
            raise serializers.ValidationError({
                'error':"Password And Confirm Password Doesn't Matched"

            })
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    'error':'Email Already Exists'
                }
            )
        account=User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
           
            )
        
        account.set_password(password)
        account.is_active=False
        account.save()
        UserProfile.objects.create(user=account,mobile_no=mobile_no, address=address,account_type=account_type)
        return account
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()





class UpdateUserProfileSerializer(serializers.ModelSerializer):
    mobile_no = serializers.CharField(source="userprofile.mobile_no", max_length=12, required=False)
    address = serializers.CharField(source="userprofile.address", max_length=100, required=False)
    account_type = serializers.ChoiceField(
        source="userprofile.account_type", 
        choices=Account_type, 
        required=False, 
        read_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile_no', 'address', 'account_type']
        read_only_fields = ['username','email','account_type']

    def update(self, instance, validated_data):
        # Update User fields
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update UserProfile fields
        userprofile_data = validated_data.get('userprofile', {})
        userprofile = instance.userprofile
        userprofile.mobile_no = userprofile_data.get('mobile_no', userprofile.mobile_no)
        userprofile.address = userprofile_data.get('address', userprofile.address)

        instance.save()
        userprofile.save()

        return instance
