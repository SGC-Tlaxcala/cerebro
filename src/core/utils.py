# coding: utf-8
#         app: cmi
#      module: core.utils
#        date: lunes, 28 de mayo de 2018 - 14:07
# description: Funciones, clases y objetos comunes
# pylint: disable=W0613,R0201,R0903

from datetime import date
from workdays import networkdays


INICIO_PROCESO = date(2017, 9, 1)
FINAL_PROCESO = date(2018, 8, 31)
HOLIDAYS = [
    date(year=2017, month=1, day=1),
    date(year=2017, month=2, day=6),
    date(year=2017, month=2, day=24),
    date(year=2017, month=3, day=20),
    date(year=2017, month=4, day=13),
    date(year=2017, month=4, day=14),
    date(year=2017, month=5, day=1),
    date(year=2017, month=5, day=10),
    date(year=2017, month=9, day=2),
    date(year=2017, month=12, day=12),
    date(year=2017, month=12, day=25),
    date(year=2018, month=1, day=1),
    date(year=2018, month=2, day=5),
    date(year=2018, month=2, day=24),
    date(year=2018, month=3, day=19),
    date(year=2018, month=3, day=29),
    date(year=2018, month=3, day=30),
    date(year=2018, month=5, day=1),
    date(year=2018, month=5, day=10),
    date(year=2018, month=11, day=2),
    date(year=2018, month=11, day=19),
    date(year=2018, month=12, day=1),
    date(year=2018, month=12, day=12),
    date(year=2018, month=12, day=25)
]


def delta(inicio, final):
    if (inicio is None) or (final is None):
        return None
    else:
        if INICIO_PROCESO < inicio < FINAL_PROCESO:
            return (final - inicio).days
        else:
            return networkdays(inicio, final, HOLIDAYS)
