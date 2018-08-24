from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse
from django.contrib.auth import get_user_model
import locale
locale.setlocale( locale.LC_ALL, 'es_MX.UTF-8' )
User = get_user_model()

register = template.Library()

@register.filter(name='jsdate')
def jsdate(d):
    """formats a python date into a js Date() constructor.
    """
    try:
        # return "new Date({0},{1},{2})".format(d.year, d.month - 1, d.day)
        return "Date.UTC({0},{1},{2})".format(d.year, d.month - 1, d.day)
    except AttributeError:
        return 'null'

@register.filter(name='remesa')
def remesa(fecha):
    '''Devuelve una remsa, dada una fecha cualquiera'''
    try:
        from core.models import Remesa
        for rem in Remesa.objects.all():
            if fecha >= rem.inicio and fecha <= rem.fin:
                return rem.remesa
    except:
        return None

@register.filter(name='moneda')
def moneda(pesos):
    pesos = round(float(pesos), 2)
    return "$%s%s" % (intcomma(int(pesos)), ("%0.2f" % pesos)[-3:])

@register.filter(name="money")
def money(lana):
    return locale.currency(lana, grouping=True )


@register.filter(name='atributo')
def atributo(calif):
    if calif <= 1: return 'bajo'
    if calif == 2: return 'medio'
    if calif == 3: return 'alto'

@register.filter(name='campos')
def campos(evidencia):
    e = evidencia
    m = evidencia.meta
    modelo = m.modelo()
    champs=[]
    fields = eval('[uno.name for uno, dos in evidencia.%s._meta.get_fields_with_model() if (dos is None)]' % modelo )
    for f in fields[1:]:
        champs.append((f, eval('evidencia.%s.%s' % (modelo, f))))
    return champs


@register.filter(name='stars')
def stars(calif):
    star = '<i class="fa fa-star"></i> '
    if calif <= 1: return star * 1
    if calif == 2: return star * 2
    if calif == 3: return star * 3

@register.simple_tag
def active(request, pattern):
    import re
    try:
        ruta = request.path
        if re.search(pattern, ruta):
            return 'active'
    except: return ''

@register.filter(name='clave')
def clave(dicc, key):
    try: return dicc[key]
    except KeyError: return 0

@register.filter(name='edita_evidencia')
def edita_evidencia(pipol, evidencia):
    url = '<a title="Editar la evidencia" href="/metas/evidencias/editar/%s/" class="btn btn-primary btn-xs" type="button"><i class="fa fa-pencil"></i></a>' % evidencia.id
    if pipol.is_superuser or (pipol.has_perm('metas.change_%s' % evidencia.meta.modelo().lower() ) and pipol == evidencia.usuario):
        return url
    else:
        return ''

@register.filter(name='borra_evidencia')
def borra_evidencia(pipol, evidencia):
    url = reverse('borrar_evidencia', kwargs={'id':evidencia.id})
    dialogo = '''<a title="Borrar la evidencia" href="javascript:confirmDelete('%s')" class="btn btn-danger btn-xs" type="button"><i class="fa fa-eraser"></i></a>''' % url
    if pipol.is_superuser or (pipol.has_perm('metas.delete_%s' % evidencia.meta.modelo().lower() ) and pipol == evidencia.usuario):
        return dialogo
    else:
        return ''

@register.filter(name='fmeta')
def fmeta(pipol, meta):
    permiso = 'metas.add_%s' % meta.lower()
    if pipol.has_perm(permiso):
        return True
    else:
        return False

@register.filter(name='porciento')
def porciento(num):
    if float(num) > 100: return 100
    else: return "%.2f" % float(num)

@register.filter(name='ceros')
def cero(num):
    if num=='' : num = 0
    return num

@register.simple_tag
def mac(mac1, mac2, var):
    if mac1 == mac2:
        dat = var
    else:
        dat = 0
    return dat

DIA = 86400

@register.filter(name='horas')
def horas(sec):
    if sec == '': return 0
    else: return (sec)/60/60

@register.filter(name='dias')
def dias(sec):
    try: return (sec)/DIA
    except TypeError: return 0
    # if sec == '': return 0
    # else: return (sec)/DIA

@register.filter(name='txthoras')
def txthoras(sec):
    if sec == '': return ''
    else:
        sec= int(sec)
        horas = ""
        tiempo = sec / 60
        d = (tiempo) / 1440
        h = (tiempo - (d * 1440)) / 60
        m = tiempo % 60
        if d > 0: horas = str(d) + 'd '
        if h > 0: horas = horas  + str(h) + "h "
        if m > 0: horas = horas  + str(m) + 'm'
        return horas

@register.filter(name='upp')
def upp(txt):
    altas = txt
    return altas.upper()

@register.filter(name='barrita')
def barrita(acuerdos, completos):
    porcentaje = float(completos) / float(acuerdos) * 100
    return porcentaje

@register.filter
def getattr (obj, args):
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
        return  obj.__dict__.get(attribute, default)
    except:
        return default
