# coding: utf-8
#         app: docs
#      module: models
#        date: miércoles, 06 de junio de 2018 - 09:08
# description: control de documentos y registros
# pylint: disable=W0613,R0201,R0903


from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Tipo (models.Model):
    tipo = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return f'Tipo: {self.tipo}'


class Proceso (models.Model):
    proceso = models.CharField(max_length=80)
    slug = models.CharField(max_length=80)

    def __str__(self):
        if self.slug == 'sgc':
            return 'Documentos del Sistema'
        elif self.slug == 'stn':
            return 'Opiniones Técnicas de la STN'
        elif self.slug == 'coc':
            return 'Oficios de la COC'
        else:
            return f'Proceso {self.proceso}'


class Documento (models.Model):
    """Definición del Documento:
    - nombre: El nombre del documento
    - slug: Un nombre corto para identificar el documento
    - ruta: Un campo URL, útil para documentos externos (opcional)
    - activo: Campo lógico, True por default
    - proceso: Contenedor para indicar el proceso al que pertenece
    - tipo: Contenedor para indicar el tipo de documento"""
    # Identificación
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)

    # Ruta
    ruta = models.URLField(blank=True, null=True)

    # Orden
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

    # Búsqueda
    activo = models.BooleanField(default=True)
    texto_ayuda = models.TextField(blank=True)

    # Trazabilidad
    autor = models.ForeignKey(User, related_name='docs', editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tipo', 'id']

    def ext(self):
        return self.revision_actual().archivo.name.split('.')[-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Documento, self).save(*args, **kwargs)

    def clave(self):
        """Devuelve la clave del documento, que es única y se forma por
        el tipo de documento (tres letras) y la identificación del documento"""
        return "%s-%02d" % (self.tipo.slug, self.id)

    def __str__(self):
        return "%s (%s-%02d)" % (self.nombre, self.tipo.slug.upper(), self.id)

    def revision_actual(self):
        """Devuelve la revisión del documento como un entero"""
        try:
            return self.revision_set.latest('revision')
        except IndexError:
            return ""

    def r_actual(self):
        """Devuelve la revisión de un documento con ceros a la izquierda"""
        try:
            x = "%02d" % self.revision_set.order_by('-revision')[0].revision
            return x
        except IndexError:
            return ""

    def historial(self):
        return self.revision_set.order_by('-revision')[1:]

    def swf(self):
        return "%s.swf" % self.revision_set.latest('revision').archivo.url.split('.')[0]


# Función para subir archivos
def subir_documento(instancia, archivo):
    import os.path
    ext = archivo.split('.')[-1]
    orig = 'docs'
    tipo = instancia.documento.tipo.slug
    doc = instancia.documento.slug
    rev = instancia.revision
    nombre = "%s_%s-%02d_rev%02d.%s" % (doc, tipo, instancia.documento.id, rev, ext)
    ruta = os.path.join(orig, tipo, nombre)
    return ruta


class Revision (models.Model):
    # Documento
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)

    # Revisión y actualización
    revision = models.IntegerField()
    f_actualizacion = models.DateField()

    # Archivos de la revisión
    archivo = models.FileField(upload_to=subir_documento, blank=True, null=True)

    # Identificación de cambios
    cambios = models.TextField()

    # Trazabilidad
    autor = models.ForeignKey(User, related_name='revisions_user', editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s rev %02d (%s)" % (self.documento, self.revision, self.f_actualizacion)

    class Meta:
        unique_together = (("documento", "revision"),)
        verbose_name = "Revisión"
        verbose_name_plural = "Control Revisiones"
