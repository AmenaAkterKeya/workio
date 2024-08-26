from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('user', views.CustomUserViewset, basename='user') 

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/', views.CustomDetail.as_view(), name='user-detail'),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]