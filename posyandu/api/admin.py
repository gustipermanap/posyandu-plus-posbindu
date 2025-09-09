from django.contrib import admin

# Register your models here.
from .models import Posyandu, Anak, Penimbangan

admin.site.register(Posyandu)
admin.site.register(Anak)
admin.site.register(Penimbangan)
