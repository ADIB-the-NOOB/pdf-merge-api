
"""pdfMergerAPI URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage.as_view()),
    path('admin/', admin.site.urls),
    path('pdfMergeAPI/', views.pdfMergerAPI.as_view()),
    path('addUser/', views.addUser.as_view()),
    path('resetPassword/', views.resetPassword.as_view()),
    path('showItdQuery/', views.showItdQuery.as_view()),
    path('distributeCoupon/', views.distributeCoupon.as_view()),
]
