from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import Idea
from .forms import IdeaForm


class IdeasIndex(ListView):
    model = Idea
    template_name = 'ideas/index.html'


class IdeaDetail(DetailView):
    model = Idea
    template_name = 'ideas/detail.html'
    context_object_name = 'idea'


class IdeaAdd(CreateView):
    model = Idea
    template_name = 'ideas/add.html'
    form_class = IdeaForm
    success_url = reverse_lazy('ideas:index')


# TODO: Add views for Idea creation, editing, and deletion
# TODO: Add views for Idea voting
# TODO: Add views for Idea comment creation, editing, and deletion
# TODO: Add views for Idea comment voting
# TODO: Add views for Idea comment reply creation, editing, and deletion
# TODO: Add views for Idea comment reply voting
