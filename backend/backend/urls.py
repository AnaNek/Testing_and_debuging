"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from backend import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

schema_view = get_schema_view(
    openapi.Info(
        title="Protein Research API",
        default_version='v1',
        description="API for service Protein Research ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="neknas28@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include("app.urls")),
    #path('api-token-auth/', obtain_jwt_token),
    #path('api-token-refresh/', refresh_jwt_token),
    #path('api-token-verify/', verify_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
