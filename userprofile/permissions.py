from rest_framework.permissions import BasePermission,SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from orders.models import Order






class IsSeller(BasePermission):
    def has_permission(self, request, view):  # Added 'view' as the second argument
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated. Please log in.")
        return request.user.userprofile.account_type == 'Seller'
    



class IsBuyerAndSeller(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated. Please log in.")
         
        if_buy=Order.objects.filter(user=request.user)
        is_seller=request.user.userprofile.account_type=='Seller'
        if if_buy or is_seller:
            return True
        
