from django.contrib import admin

from FoodCaloEstimate.estimator.admin_models.my_input_image_admin import MyInputImageAdmin
from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage

# Register your models here.

admin.site.register(MyInputImage, MyInputImageAdmin)
