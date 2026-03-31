from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portal import views
from django.conf.urls import handler500, handler404, handler403

urlpatterns = [
    path('admin-portal/', admin.site.urls),
    path('', include('portal.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler500 = views.error500
handler404 = views.error404
handler403 = views.error403