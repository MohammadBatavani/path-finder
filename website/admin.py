from django.contrib import admin
from .models import Map, Map_Thread, History, Algorithm

# Register your models here.
admin.site.register(Map)
admin.site.register(Map_Thread)
admin.site.register(History)
admin.site.register(Algorithm)