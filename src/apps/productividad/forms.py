# coding: utf-8
#         app: productividad
#      module: forms
#        date: viernes, 29 de junio de 2018 - 12:57
# description: Formularios
# pylint: disable=W0613,R0201,R0903

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms
from django.forms.models import inlineformset_factory

from apps.productividad.models import ReporteSemanal, Cifras


class CifrasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CifrasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('modulo', wrapper_class='col'),
                Field('dias_trabajados', wrapper_class='col'),
                Field('jornada', wrapper_class='col'),
                Field('tramites', wrapper_class='col'),
                Field('cred_recibidas', wrapper_class='col'),
                Field('cred_entregadas', wrapper_class='col'),
                css_class='row'
            )
        )

    class Meta:
        model = Cifras
        fields = '__all__'


class ReporteSemanalForm(forms.ModelForm):

    class Meta:
        model = ReporteSemanal
        fields = '__all__'


ReporteCifrasFormSet = inlineformset_factory(
    ReporteSemanal,
    Cifras,
    form=CifrasForm,
    can_delete=False,
    extra=11
)
