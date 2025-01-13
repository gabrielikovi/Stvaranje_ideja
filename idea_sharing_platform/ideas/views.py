from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Idea
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def add_user_to_group(user_id, group_name):
    try:
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        return f"Korisnik {user.username} dodan u grupu {group_name}."
    except User.DoesNotExist:
        return "Korisnik ne postoji."
    except Group.DoesNotExist:
        return "Grupa ne postoji."


class IdeaListView(ListView):
    model = Idea
    template_name = 'idea_list.html'
    context_object_name = 'ideas'
    paginate_by = 10  # Opcionalno: Paginacija

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')  # Preuzmi parametar pretraživanja iz URL-a
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea_detail.html'
    context_object_name = 'idea'

class IdeaCreateView(CreateView):
    model = Idea
    template_name = 'idea_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('idea_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IdeaUpdateView(UpdateView):
    model = Idea
    template_name = 'idea_form.html'
    fields = ['title', 'description']

    def get_success_url(self):
        return reverse_lazy('idea_detail', kwargs={'pk': self.object.pk})


class IdeaDeleteView(DeleteView):
    model = Idea
    template_name = 'idea_confirm_delete.html'
    success_url = reverse_lazy('idea_list')