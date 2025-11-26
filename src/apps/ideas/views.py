from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import IdeaForm
from .models import Idea, Resolve, IDEA, PROJECT, VIABLE


class IdeasIndex(ListView):
    model = Idea
    template_name = 'ideas/index.html'
    context_object_name = 'ideas'

    def get_queryset(self):
        return (
            Idea.objects.prefetch_related(
                Prefetch('resolve_set', queryset=Resolve.objects.order_by('-created'))
            )
            .order_by('-created')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ideas = list(context['ideas'])
        context['ideas'] = ideas
        total = len(ideas)
        ideas_count = sum(1 for idea in ideas if idea.type == IDEA)
        projects_count = sum(1 for idea in ideas if idea.type == PROJECT)
        viable_count = sum(
            1
            for idea in ideas
            if idea.latest_resolution and idea.latest_resolution.viable == VIABLE
        )
        context['stats'] = {
            'total': total,
            'ideas': ideas_count,
            'projects': projects_count,
            'viable': viable_count,
        }
        return context


class IdeaDetail(DetailView):
    model = Idea
    template_name = 'ideas/detail.html'
    context_object_name = 'idea'

    def get_queryset(self):
        return Idea.objects.prefetch_related(
            Prefetch('resolve_set', queryset=Resolve.objects.order_by('-created'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resolution'] = self.object.latest_resolution
        return context


class IdeaAdd(CreateView):
    model = Idea
    template_name = 'ideas/add.html'
    form_class = IdeaForm
    success_url = reverse_lazy('ideas:index')

    def form_valid(self, form):
        messages.success(self.request, '¡Gracias! Tu idea fue recibida correctamente.')
        return super().form_valid(form)


# TODO: Add views for Idea creation, editing, and deletion
# TODO: Add views for Idea voting
# TODO: Add views for Idea comment creation, editing, and deletion
# TODO: Add views for Idea comment voting
# TODO: Add views for Idea comment reply creation, editing, and deletion
# TODO: Add views for Idea comment reply voting
