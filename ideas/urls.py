from django.urls import path, include
from django.contrib.auth import views as auth_views
from ideas import views
from rest_framework.routers import DefaultRouter
from .views import IdeaListView, IdeaViewSet
from django.shortcuts import redirect

router = DefaultRouter()
router.register(r'ideas', IdeaViewSet, basename='ideas')

def redirect_to_login(request):
    return redirect('login/')

urlpatterns = [
    path('', redirect_to_login),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ideas/', IdeaListView.as_view(), name='idea_list'),
    path('ideas/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('ideas/new/', views.IdeaCreateView.as_view(), name='idea_create'),
    path('ideas/<int:pk>/edit/', views.IdeaUpdateView.as_view(), name='idea_update'),
    path('ideas/<int:pk>/delete/', views.IdeaDeleteView.as_view(), name='idea_delete'),
    path('api/', include(router.urls)),
]
