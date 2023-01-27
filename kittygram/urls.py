from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.contrib import admin

from django.urls import include, path

from cats.views import CatViewSet, UserViewSet, LightCatViewSet


router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', UserViewSet)
router.register(r'mycats', LightCatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('api-token-auth/', views.obtain_auth_token),
    # базовые-эндпоинты, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]


