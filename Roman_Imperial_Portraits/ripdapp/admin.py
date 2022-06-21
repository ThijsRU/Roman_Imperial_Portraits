from django.contrib import admin

# Register your models here.
from ripdapp.models import Portrait, Information


admin.site.register(Portrait)
admin.site.register(Information)