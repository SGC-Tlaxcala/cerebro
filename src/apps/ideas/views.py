from django.views.generic import TemplateView


class IdeasIndex(TemplateView):
    template_name = 'ideas/index.html'


class IdeasList(TemplateView):
    template_name = 'ideas/ideas.html'
