from django.contrib import admin

# Register your models here.

from .models import Myuser,Material

admin.site.register(Myuser)
admin.site.register(Material)
