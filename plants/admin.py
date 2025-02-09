from django.contrib import admin

# Register your models here.
from . models import Plants, Blog

# Register your models here.
class PlantsAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','category','seller_name']


    def seller_name(self, obj):
        # Ensure obj.seller is not None before trying to access its attributes
        if obj.seller:
            return f"{obj.seller.user.username}"
        return None
    

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','author_name','created_at']

    def author_name(self, obj):
        if obj.author:
            return f"{obj.author.user.username}"
        return None
    

admin.site.register(Blog, BlogAdmin)

admin.site.register(Plants,PlantsAdmin)