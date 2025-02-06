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
        
        # Check if user is either a seller or a buyer with orders
        is_seller = request.user.userprofile.account_type == 'Seller'
        has_orders = Order.objects.filter(user=request.user).exists()
        
        # Allow if user is a seller or a buyer with orders
        if is_seller or has_orders:
            return True
        
        raise PermissionDenied("User is neither a buyer nor a seller.")
        
