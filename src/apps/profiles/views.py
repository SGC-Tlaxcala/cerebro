import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import serializers as drf_serializers

from .forms import QuickUserProfileForm


class UserQuickCreateView(LoginRequiredMixin, View):
    template_name = 'profiles/partials/_user_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied = not request.user.is_superuser
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = None if self.permission_denied else QuickUserProfileForm()
        status_code = 403 if self.permission_denied else 200
        return render(request, self.template_name, self.get_context_data(form), status=status_code)

    def post(self, request, *args, **kwargs):
        if self.permission_denied:
            return render(request, self.template_name, self.get_context_data(None), status=403)

        form = QuickUserProfileForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except drf_serializers.ValidationError as exc:
                self._attach_serializer_errors(form, exc.detail)
            else:
                payload = json.dumps({
                    'pas:user-created': {
                        'id': user.pk,
                        'label': QuickUserProfileForm.display_name(user),
                        'email': user.email,
                    },
                    'profiles:close-modal': '',
                })
                return HttpResponse('', status=204, headers={'HX-Trigger': payload})
        return render(request, self.template_name, self.get_context_data(form), status=422)

    def get_context_data(self, form):
        return {
            'form': form,
            'form_action': reverse('profiles:user-quick-add'),
            'permission_denied': self.permission_denied,
        }

    @staticmethod
    def _attach_serializer_errors(form, detail):
        if isinstance(detail, dict):
            for field, errors in detail.items():
                if field == 'profile' and isinstance(errors, dict):
                    for sub_field, sub_errors in errors.items():
                        for message in UserQuickCreateView._as_list(sub_errors):
                            form.add_error(sub_field, message)
                else:
                    for message in UserQuickCreateView._as_list(errors):
                        form.add_error(field if field in form.fields else None, message)
        else:
            for message in UserQuickCreateView._as_list(detail):
                form.add_error(None, message)

    @staticmethod
    def _as_list(value):
        if isinstance(value, (list, tuple)):
            return value
        return [value]
