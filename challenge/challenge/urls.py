from django.contrib import admin
from django.urls import path, include
from myserver.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("myserver/users/signup/", CreateUserView.as_view(), name="signup"),  
    path("myserver/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("myserver/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("myserver-auth/", include("rest_framework.urls")),
]