from django.views.generic import ListView
from django.views.generic import DetailView

from apps.ideas.models import Idea


class IdeasIndex(ListView):
    model = Idea
    template_name = 'ideas/index.html'


class IdeaDetail(DetailView):
    model = Idea
    template_name = 'ideas/detail.html'
    context_object_name = 'idea'


TODO: Add views for Idea creation, editing, and deletion
TODO: Add views for Idea voting
TODO: Add views for Idea comment creation, editing, and deletion
TODO: Add views for Idea comment voting
TODO: Add views for Idea comment reply creation, editing, and deletion
TODO: Add views for Idea comment reply voting