"""django_chat URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from .views import home_chat_view,group_chat_view
from allauth.account.views import LoginView
login = LoginView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^home_chat/$',home_chat_view,name='home'),    
    re_path(r'^home_groups/$',group_chat_view,name='home_groups'),    
    path("", login, name="account_login"),
    path('accounts/', include('allauth.urls')),
    path('accounts_/', include('accounts.urls')),
    path('chats/', include('chats.urls')),
    re_path('groups/', include('groups.urls')),
]
