from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model=CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["id", "car_maker", "name", "type", "year"]        

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    inlines = [ CarModelInline ]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)