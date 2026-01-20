from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    # Campos que verás en la tabla principal
    # 'email_full' funciona aquí porque Django reconoce propiedades del modelo
    list_display = (
        "nombre_completo",
        "usuario_inst",
        "email_full",
        "is_active",
        "created_at",
    )

    # Filtros laterales para gestión rápida
    list_filter = ("is_active", "created_at")

    # Buscador por nombre o usuario
    search_fields = ("nombre_completo", "usuario_inst")

    # Ordenar por los más recientes primero
    ordering = ("-created_at",)

    # Campos de solo lectura al editar un registro
    readonly_fields = ("token", "created_at")

    # --- TUS "PODEROSAS MANOS": ACCIONES MASIVAS ---
    actions = ["activar_suscriptores", "desactivar_suscriptores"]

    @admin.action(description="✅ Activar seleccionados (Validación SGC)")
    def activar_suscriptores(self, request, queryset):
        filas_actualizadas = queryset.update(is_active=True)
        self.message_user(
            request, f"¡Éxito! {filas_actualizadas} suscriptores han sido activados."
        )

    @admin.action(description="❌ Desactivar seleccionados")
    def desactivar_suscriptores(self, request, queryset):
        filas_actualizadas = queryset.update(is_active=False)
        self.message_user(
            request, f"Se han desactivado {filas_actualizadas} registros."
        )
