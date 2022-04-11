from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view),
    path('', main_view, name='main_view'),
    path('calculate/', calculate_view),
    path('signOut/', signOut),
    path('switch/', switch),
    path('static/',static),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
