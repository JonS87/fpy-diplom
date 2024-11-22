from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FileViewSet, login_user, register_user,download_file_by_special_link

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'files', FileViewSet, basename='files')

urlpatterns = [
    path('auth/login/', login_user, name='login_user'),
    path('auth/register/', register_user, name='register_user'),
    path('download/<str:special_link>/', download_file_by_special_link, name='download_file'),

    path('', include(router.urls)),
]
