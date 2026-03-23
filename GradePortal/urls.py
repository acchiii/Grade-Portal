from django.contrib import admin
from django.urls import path, include
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
]
