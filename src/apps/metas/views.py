# coding: utf-8
#         app: metas
#      module: views
#        date: miércoles, 23 de mayo de 2018 - 11:05
# description: Vistas para las metas
# pylint: disable=W0613,R0201,R0903

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Role, Site, Member, Goal, Proof
from .forms import AddRolForm, AddSiteForm, AddMemberForm, AddGoalForm, ProofForm


class MetasIndex(TemplateView):
    template_name = 'metas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = Member.objects.all().order_by('role__order')
        context.update({'members': members})
        return context


class MetasAddGoal(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = AddGoalForm
    success_url = reverse_lazy('metas:add_goal')

    def get_context_data(self, **kwargs):
        context = super(MetasAddGoal, self).get_context_data(**kwargs)
        goals = Goal.objects.all().order_by('role__order')
        context.update({'goals': goals})
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        print(self.request.user)
        return super(MetasAddGoal, self).form_valid(form)


class MetasAddMember(LoginRequiredMixin, CreateView):
    model = Member
    form_class = AddMemberForm
    success_url = reverse_lazy('metas:add_member')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = Member.objects.all().order_by('role__order')
        context.update({'members': members})
        return context


class MetasAddSite(LoginRequiredMixin, CreateView):
    model = Site
    form_class = AddSiteForm
    success_url = reverse_lazy('metas:add_site')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sites = Site.objects.all()
        context.update({'sites': sites})
        return context


class MetasAddRole(LoginRequiredMixin, CreateView):
    model = Role
    form_class = AddRolForm
    success_url = reverse_lazy('metas:add_role')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roles = Role.objects.all().order_by('order')
        context.update({'kpi_path': True, 'roles': roles})
        return context


class CreateProof(LoginRequiredMixin, CreateView):
    model = Proof
    form_class = ProofForm
    success_url = reverse_lazy('metas:add_proof')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        print(self.request.user)
        return super(CreateProof, self).form_valid(form)
