# coding: utf-8
#         app: mx.ine.tlx.sgc.cerebro.profiles
#      módulo: profiles.models
# descripción: Add profile info to User model
#       autor: Javier Sanchez Toledano
#       fecha: lunes, mayo 21 de 2018

import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


TLAXCALA = 29
ENTIDADES = (
    (TLAXCALA, 'Tlaxcala'),
)

JL = 0
JD01 = 1
JD02 = 2
JD03 = 3
SITIO = (
    (JL, 'Junta Local'),
    (JD01, '01 Junta Distrital'),
    (JD02, '02 Junta Distrital'),
    (JD03, 'O3 Junta Distrital')
)

VEL = 'VEL'
VSL = 'VSL'
VRL = 'VRL'
VOL = 'VOL'
VCL = 'VCL'
VED = 'VED'
VSD = 'VSD'
VRD = 'VRD'
VOD = 'VOD'
VCD = 'VCD'
JMM = 'JMM'
JOSA = 'JOSA'
JOSAD = 'JOSAD'
JOCE = 'JOCE'
RA = 'RA'

PUESTOS = (
    (VEL, 'Vocal Ejecutivo de Junta Local'),
    (VSL, 'Vocal Secretario de Junta Local'),
    (VRL, 'Vocal del RFE de Junta Local'),
    (VCL, 'Vocal de Capacitación de Junta Local'),
    (VOL, 'Vocal de Organización de Junta Local'),
    (VED, 'Vocal Ejecutivo de Junta Distrital'),
    (VSD, 'Vocal Secretario de Junta Distrital'),
    (VRD, 'Vocal del RFE de Junta Distrital'),
    (VCD, 'Vocal de Capacitación de Junta Distrital'),
    (VOD, 'Vocal de Organización de Junta Distrital'),
    (JOSA, 'JOSA'),
    (JOSAD, 'JOSAD'),
    (JMM, 'Jefe de Monitoreo a Módulos'),
    (JOCE, 'Jefe de Cartografía'),
    (RA, 'Rama Administrativa')
)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(choices=ENTIDADES, default=TLAXCALA)
    site = models.PositiveSmallIntegerField(choices=SITIO, default=0)
    position = models.CharField(choices=PUESTOS, max_length=5, default=RA)
    order = models.PositiveSmallIntegerField(default=99, blank=True, null=True)
    recibe_notificaciones = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
