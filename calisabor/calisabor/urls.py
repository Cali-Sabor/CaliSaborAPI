"""calisabor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken import views
from api.auth import Login, Logout, Register, ResetPassword


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'))),
    path('gen_token/', views.obtain_auth_token),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view())),
    path('register/', login_required(Register.as_view())),
    path('reset-password/', login_required(ResetPassword.as_view())),
]
