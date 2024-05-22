from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views


urlpatterns = [
   # path('', include(router.urls)),
   path('register/', views.RegistrationViewSet.as_view(), name='register'),
   path('active/<uid64>/<token>/', views.activate, name='activate'),
   path('login/', views.LoginViewSet.as_view(), name='login'),
   path('logout/', views.logout_view,name='logout'),
   path('profile/', views.UserProfileViewSet.as_view(), name='profile'),
]
