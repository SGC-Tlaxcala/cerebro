- [x] 8. Crear pruebas unitarias para `build_cmi_portatil.py`.
    - [x] 8.1 Verificar ejecución exitosa y generación de directorio.
    - [x] 8.2 Verificar contenido del manifiesto y archivos copiados.

- [x] 9. Agregar tiempo de ejecución a la salida de `build_cmi_portatil.py`.


Este documento rastrea el progreso de las tareas de refactorización y desarrollo.

- [x] 1. Asegurar que solo se listen documentos activos en la app `docs`.
    - [x] 1.1 Modificar `Buscador` en `views.py` para filtrar `activo=True`.
    - [x] 1.2 Modificar `DocumentViewSet` en `api/views.py` para filtrar `activo=True` por defecto.
    - [x] 1.3 Agregar pruebas para verificar que no aparezcan documentos inactivos.
- [x] 2. Hacer públicas las vistas de consulta de PAS.
    - [x] 2.1 Remover `login_required` de vistas de solo lectura en `pas/views.py`.
    - [x] 2.2 Ocultar controles de escritura en templates de PAS para usuarios anónimos.
- [x] 3. Optimizar visualización de Tipo de Plan en listado PAS.
    - [x] 3.1 Agregar propiedad `siglas` al modelo `Plan`.
    - [x] 3.2 Actualizar template `pas/index.html` para mostrar siglas.
- [x] 4. Configurar editor para evitar rupturas de línea en templates.
    - [x] 4.1 Configurar `html.format.wrapLineLength: 0` en `.vscode/settings.json`.

- [ ] 5. Mejorar visualización de estado 'Fuera de tiempo' en PAS.
    - [x] 5.1 Reemplazar texto por icono de alerta rojo en index.
    - [x] 5.2 Reemplazar texto 'Cerrada' por icono check-badge azul filled.

- [x] 6. Refactorizar generate_manifest.py como management command.
    - [x] 6.1 Transformar script en BaseCommand.
    - [x] 6.2 Generar pruebas unitarias para el comando.

