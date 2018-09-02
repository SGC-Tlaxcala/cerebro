from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse
import locale

locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')
register = template.Library()
DIA = 86400

INTERVALOS = (
    ('semanas', 604800),  # 60 * 60 * 24 * 7
    ('días', 86400),    # 60 * 60 * 24
    ('horas', 3600),    # 60 * 60
    ('minutos', 60),
    ('segundos', 1),
    )


@register.filter(name='jsdate')
def jsdate(d):
    """formats a python date into a js Date() constructor."""
    try:
        # return "new Date({0},{1},{2})".format(d.year, d.month - 1, d.day)
        return "Date.UTC({0},{1},{2})".format(d.year, d.month - 1, d.day + 1)
    except AttributeError:
        return 'null'


@register.filter(name="mas20")
def mas20(dias):
    try:
        return dias if dias <= 20 else 20
    except TypeError:
        return None

@register.filter(name='remesa')
def remesa(fecha):
    """Devuelve una remesa, dada una fecha cualquiera"""
    from core.models import Remesa
    try:
        for rem in Remesa.objects.all():
            if rem.inicio <= fecha <= rem.fin:
                return rem.remesa
    except Remesa.DoesNotExist:
        return None


@register.filter(name='moneda')
def moneda(pesos):
    pesos = round(float(pesos), 2)
    return "$%s%s" % (intcomma(int(pesos)), ("%0.2f" % pesos)[-3:])


@register.filter(name="money")
def money(lana):
    return locale.currency(lana, grouping=True)


@register.filter(name='atributo')
def atributo(calif):
    if calif <= 1:
        return 'bajo'
    if calif == 2:
        return 'medio'
    if calif == 3:
        return 'alto'


@register.filter(name='campos')
def campos(evidencia):
    m = evidencia.meta
    modelo = m.modelo()
    champs = []
    fields = eval('[uno.name for uno, dos in evidencia.%s._meta.get_fields_with_model() if (dos is None)]' % modelo)
    for f in fields[1:]:
        champs.append((f, eval('evidencia.%s.%s' % (modelo, f))))
    return champs


@register.filter(name='stars')
def stars(calif):
    star = '<i class="fa fa-star"></i> '
    if calif <= 1:
        return star * 1
    if calif == 2:
        return star * 2
    if calif == 3:
        return star * 3


@register.simple_tag
def active(request, pattern):
    import re
    try:
        ruta = request.path
        if re.search(pattern, ruta):
            return 'active'
    except re.error:
        return ''


@register.filter(name='clave')
def clave(dic, key):
    try:
        return dic[key]
    except KeyError:
        return 0


@register.filter(name='edita_evidencia')
def edita_evidencia(usuario, evidencia):
    url = '<a title="Editar la evidencia" \
        href="/metas/evidencias/editar/%s/" \
        class="btn btn-primary btn-xs" type="button">\
        <i class="fa fa-pencil"></i></a>' % evidencia.id
    if usuario.is_superuser or (
        usuario.has_perm(
            'metas.change_%s' % evidencia.meta.modelo().lower()
            ) and usuario == evidencia.usuario):
        return url
    else:
        return ''


@register.filter(name='borra_evidencia')
def borra_evidencia(usuario, evidencia):
    url = reverse('borrar_evidencia', kwargs={'id': evidencia.id})
    dialogo = '''<a title="Borrar la evidencia" \
        href="javascript:confirmDelete('%s')" \
        class="btn btn-danger btn-xs" type="button">\
        <i class="fa fa-eraser"></i></a>''' % url
    if usuario.is_superuser or \
        (usuario.has_perm('metas.delete_%s' % evidencia.meta.modelo().lower()) and
         usuario == evidencia.usuario):
        return dialogo
    else:
        return ''


@register.filter(name='fmeta')
def fmeta(persona, meta):
    permiso = 'metas.add_%s' % meta.lower()
    if persona.has_perm(permiso):
        return True
    else:
        return False


@register.filter(name='porcentaje')
def porcentaje(num):
    return "%.2f" % float(num)


@register.filter(name='porciento')
def porciento(num):
    if float(num) > 100:
        return 100
    else:
        return "%.2f" % float(num)


@register.filter(name='ceros')
def cero(num):
    if num == '':
        num = 0
    return num


@register.simple_tag
def mac(mac1, mac2, var):
    if mac1 == mac2:
        dat = var
    else:
        dat = 0
    return dat


@register.filter(name='horas')
def horas(sec):
    if sec == '':
        return 0
    else:
        return sec/60/60


@register.filter(name='dias')
def dias(sec):
    try:
        return sec/DIA
    except TypeError:
        return 0


@register.filter(name='txthoras')
def txthoras(delta):
    if delta == '':
        return ''
    else:
        resultado = []
        for name, count in INTERVALOS:
            valor = delta // count
            if valor:
                delta -= valor * count
                if valor == 1:
                    name = name.rstrip('s')
                resultado.append("{} {}".format(int(valor), name))
        return ', '.join(resultado[:2])


@register.filter(name='upp')
def upp(txt):
    altas = txt
    return altas.upper()


@register.filter(name='barrita')
def barrita(acuerdos, completos):
    fill = float(completos) / float(acuerdos) * 100
    return fill


@register.filter
def get_attr(obj, args):
    """ Try to get an attribute from an object.

    Example: {% if block|getattr:"editable,True" %}

    Beware that the default is always a string, if you want this
    to return False, pass an empty second argument:
    {% if block|getattr:"editable," %}
    """
    args = args.split(',')
    if len(args) == 1:
        (attribute, default) = [args[0], '']
    else:
        (attribute, default) = args
    try:
        return obj.__getattribute__(attribute)
    except AttributeError:
        return obj.__dict__.get(attribute, default)
    except KeyError:
        return default
