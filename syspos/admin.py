from django.contrib import admin
from.models import tbl_customer, tbl_user,tbl_user_types
# Register your models here.
admin.site.register(tbl_user_types)
admin.site.register(tbl_user)
admin.site.register(tbl_customer)