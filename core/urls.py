from django.conf import settings
from django.contrib import admin
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.FEATURE_SWAGGER:
    urlpatterns += [
        path('api/docs/', SpectacularSwaggerView.as_view(), name='docs'),
        path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    ]
