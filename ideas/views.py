from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Idea
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import IdeaSerializer

@login_required
def add_user_to_group(user_id, group_name):
    try:
        user = User.objects.get(id=user_id)
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)
        return f"Korisnik {user.username} dodan u grupu {group_name}."
    except User.DoesNotExist:
        return "Korisnik ne postoji."
    except Group.DoesNotExist:
        return "Grupa ne postoji."

class IdeaListView(LoginRequiredMixin, ListView):
    model = Idea
    template_name = 'idea_list.html'
    context_object_name = 'ideas'
    paginate_by = 10
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset

class IdeaDetailView(LoginRequiredMixin, DetailView):
    model = Idea
    template_name = 'idea_detail.html'
    context_object_name = 'idea'
    login_url = '/login/'

class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    template_name = 'idea_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('idea_list')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class IdeaUpdateView(LoginRequiredMixin, UpdateView):
    model = Idea
    template_name = 'idea_form.html'
    fields = ['title', 'description']
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('idea_detail', kwargs={'pk': self.object.pk})

class IdeaDeleteView(LoginRequiredMixin, DeleteView):
    model = Idea
    template_name = 'idea_confirm_delete.html'
    success_url = reverse_lazy('idea_list')
    login_url = '/login/'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group, _ = Group.objects.get_or_create(name='Korisnik')
            user.groups.add(user_group)
            login(request, user)
            messages.success(request, "Registracija uspješna! Sada ste prijavljeni.")
            return redirect('idea_list')
        else:
            messages.error(request, "Došlo je do pogreške. Pokušajte ponovno.")
    else:
        form = UserCreationForm()
    return render(request, 'register/register.html', {'form': form})

class IdeaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ideas = Idea.objects.filter(author=request.user)
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IdeaViewSet(ModelViewSet):
    serializer_class = IdeaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(author=self.request.user)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(('/login/', '/register/', '/admin/')):
            return redirect('/login/')
        return self.get_response(request)
