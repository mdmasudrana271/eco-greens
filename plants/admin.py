from django.contrib import admin

# Register your models here.
from . models import Plants

# Register your models here.
class PlantsAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','category']
    


admin.site.register(Plants,PlantsAdmin)