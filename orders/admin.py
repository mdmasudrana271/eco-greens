from django.contrib import admin
from . models import Order

# Register your models here.

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user','total_price','status','order_date','address','phone']
    


admin.site.register(Order,OrdersAdmin)