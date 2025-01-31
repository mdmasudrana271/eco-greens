from django.contrib import admin
from . models import UserProfile
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','mobile_no','account_type']
    
    def first_name(self,obj):
        return obj.user.first_name
    
    def last_name(self,obj):
        return obj.user.last_name
    def email(self,obj):
        return obj.user.email
    
    
admin.site.register(UserProfile, UserProfileAdmin)