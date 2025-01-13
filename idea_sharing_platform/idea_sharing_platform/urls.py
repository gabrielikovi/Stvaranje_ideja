"""
URL configuration for idea_sharing_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from ideas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ideas/', views.IdeaListView.as_view(), name='idea_list'),
    path('ideas/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ideas/', views.IdeaListView.as_view(), name='idea_list'),
    path('ideas/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('ideas/new/', views.IdeaCreateView.as_view(), name='idea_create'),
    path('ideas/<int:pk>/edit/', views.IdeaUpdateView.as_view(), name='idea_update'),
    path('ideas/<int:pk>/delete/', views.IdeaDeleteView.as_view(), name='idea_delete'),
]
