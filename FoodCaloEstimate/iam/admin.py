from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from FoodCaloEstimate.iam.constants.general_constants import AUTHOR

admin.site.site_header = "Food Calo Estimate Admin"
admin.site.site_title = AUTHOR
admin.site.index_title = "Hello!"

# Register your models here.
User = get_user_model()
admin.site.register(User)

admin.site.unregister(Group)
