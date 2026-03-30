from django.contrib import admin
from django.urls import path, include
from portal import views
from django.conf.urls import handler500, handler404

urlpatterns = [
    path('admin-portal/', admin.site.urls),
    path('', include('portal.urls')),
]

handler500 = views.error500
handler404 = views.error404