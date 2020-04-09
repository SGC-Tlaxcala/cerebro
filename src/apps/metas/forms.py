# coding: utf-8
#         app: metas
#      module: forms
#       fecha: miércoles, 23 de mayo de 2018 - 10:22
# description: Formularios de las Metas SPEN
# pylint: disable=W0613,R0201,R0903

from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_forms.helper import FormHelper
from django import forms

from apps.metas.models import Proof, Goal, Role, Site, Member


class ProofForm(forms.ModelForm):

    class Meta:
        model = Proof
        exclude = ['campos', ]


class AddSiteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('site', wrapper_class='col-md-2 col-sm-4'),
                Field('name', wrapper_class='col-md-5'),
                Field('address', wrapper_class='col-md-7'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Site
        fields = '__all__'


class AddRolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddRolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('clave', wrapper_class='col-md-2 col-sm-4'),
                Field('order', wrapper_class='col-md-2 col-sm-3'),
                css_class='row'
            ),
            Div(
                Field('description', wrapper_class='col-md-6'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Role
        fields = '__all__'


class AddMemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('name', wrapper_class='col-md-7'),
                css_class='row'
            ),
            Div(
                Field('mail', wrapper_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div(Field('role'), css_class='col-md-4'),
                Div(Field('site'), css_class='col-md-4'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Member
        fields = '__all__'


class AddGoalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddGoalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('role', wrapper_class='col-md-2 col-sm-6'),
                css_class='row'
            ),
            Div(
                Field('key', wrapper_class='col-md-2 col-sm-4'),
                Field('name', wrapper_class='col-md-4 col-sm-8'),
                Field('year', wrapper_class='col-md-2 col-sm-3'),
                Field('loops', wrapper_class='col-md-2 col-sm-3'),
                css_class='row'
            ),
            Div(
                Field('description', wrapper_class='col', rows='2'),
                Field('support', wrapper_class='col'),
                css_class='row'
            ),
            Div(
                Field('fields', wrapper_class='col', rows='3'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Goal
        exclude = ['user', 'created', 'updated']
