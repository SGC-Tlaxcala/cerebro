# -*- encoding: utf-8 -*-
# nombre: cmi.docs.models
#   desc: Modelos para la apps de Control de Documentos

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.template.defaultfilters import slugify
import watson

from django.contrib.auth import get_user_model
User = get_user_model()

class Tipo (models.Model):
    tipo = models.CharField (max_length = 50)
    slug = models.CharField (max_length = 50)
  
    def __unicode__ (self):
        return u'Tipo: %s' % force_unicode(self.tipo)
  
class Proceso (models.Model):
    proceso = models.CharField (max_length = 80)
    slug = models.CharField (max_length = 80)
  
    def __unicode__ (self):
        if self.slug == 'sistema': return 'Documentos del Sistema'
        else: return u'Proceso %s' % force_unicode(self.proceso)
  
class Documento (models.Model):
    '''Definición del Documento:
    - nombre: El nombre del documento
    - slug: Un nombre corto para identificar el documento
    - ruta: Un campo URL, útil para documentos externos (opcional)
    - activo: Campo lógico, True por default
    - proceso: Contenedor para indicar el proceso al que pertenece
    - tipo: Contenedor para indicar el tipo de documento'''
    # Identificación
    nombre = models.CharField     (max_length = 120)
    slug = models.SlugField       (max_length = 120) #cambio 14/05/2013
    # Ruta
    ruta = models.URLField        (blank = True, null = True)
    # Orden
    proceso = models.ForeignKey   (Proceso)
    tipo = models.ForeignKey      (Tipo)
    # Búsqueda
    activo = models.BooleanField (default=True)
    texto_ayuda = models.TextField (blank=True)
    # Trazabilidad
    autor = models.ForeignKey(User, related_name='docs', editable=False)
    creacion = models.DateTimeField(auto_now_add=True)
    actualiza = models.DateTimeField (auto_now = True)

    def ext(self):
        return self.revision_actual().archivo.name.split('.')[-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Documento, self).save(*args, **kwargs)      
        
    def clave(self):
        '''Devuelve la clave del documento, que es única y se forma por
        el tipo de documento (tres letras) y la identificacion del documento'''
        return "%s-%02d" % (self.tipo.slug, self.id) 
  
    def __unicode__ (self):
        return u"%s (%s-%02d)" % (force_unicode(self.nombre), self.tipo.slug.upper(), self.id)
  
    def revision_actual (self):
        '''Devuelve la revisión del documento como un entero'''
        try:
            x = self.revision_set.latest('revision')
            return x
        except IndexError:
            return ""
        # return self.controldocumento_set.order_by('-revision')[0]
  
    def r_actual (self):
        '''Devuelve la revisión de un documento con ceros a la izquierda'''
        try:
            x = "%02d" % self.revision_set.order_by('-revision')[0].revision
            return x
        except IndexError:
            return ""
  
    def historial (self):
        return self.revision_set.order_by('-revision')[1:]
    
def subir_archivo(instancia, archivo):
    import os.path
    import subprocess
    from cmi import settings
    tmp = os.path.join(u'/tmp/', f.name)
    destination = open(tmp, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()  
    tipo = instancia.documento.tipo.slug
    doc  = instancia.documento.slug
    rev  = instancia.revision    
    ext  = instancia.archivo.name.split('.')[-1]
    if ext=='pdf':
        archivo  = "%s_%s-%02d_rev%02d.swf" % (doc, tipo, instancia.documento.id, rev)
        salida = os.path.join(settings.MEDIA_ROOT, 'docs', tipo,  archivo)
        swftools = u'/usr/local/bin/pdf2swf'
        args = "-f -T 9 -t -s storeallcharacters"
        try: 
            subprocess.call([swftools, tmp, "-o", salida, '-f', '-T 9', '-t', '-s storeallcharacters'])
            return archivo
        except:
            raise Exception
    else:
        archivo  = "%s_%s-%02d_rev%02d.%s" % (doc, tipo, instancia.documento.id, rev, ext)
        salida = os.path.join(settings.MEDIA_ROOT, 'docs', tipo,  archivo)        
        return archivo

# Funcion para subir archivos
def subir_documento(instancia, archivo):
    import os.path
    ext = archivo.split('.')[-1]
    orig = 'docs'
    tipo = instancia.documento.tipo.slug
    doc  = instancia.documento.slug
    rev  = instancia.revision 
    nombre = "%s_%s-%02d_rev%02d.%s" % (doc, tipo, instancia.documento.id, rev, ext)
    ruta = os.path.join(orig, tipo, nombre)
    return ruta


class Revision (models.Model):
    # Docuemnto
    documento = models.ForeignKey(Documento)
    # Revisión y actualizacion
    revision = models.IntegerField ()
    f_actualizacion = models.DateField ()
    # Archivos de la revisión
    archivo = models.FileField(upload_to=subir_documento, blank = True, null = True)
    # Identificación de cambios
    cambios = models.TextField ()
    # Trazabilidad
    autor = models.ForeignKey(User, editable=False)
    creacion = models.DateTimeField(auto_now_add=True)
    actualiza = models.DateTimeField (auto_now = True)    

      
    def __unicode__ (self):
        return u"%s rev %02d (%s)" % (self.documento, self.revision, self.f_actualizacion)
    
    class Meta:
        unique_together = (("documento", "revision"),)
        verbose_name = "Revisión"
        verbose_name_plural = "Control Revisiones"


watson.register(Documento, field=('texto_ayuda', 'nombre', 'slug'))