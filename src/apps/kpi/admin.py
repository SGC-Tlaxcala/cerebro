from django.contrib import admin

from .models import *
for model in admin.site._registry.keys():
    pass  # Evita registrar modelos duplicados

for model in [m for m in locals().values() if hasattr(m, '_meta') and hasattr(m._meta, 'app_label')]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
