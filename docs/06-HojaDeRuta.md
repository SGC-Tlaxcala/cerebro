- [x] 8. Crear pruebas unitarias para `build_cmi_portatil.py`.
    - [x] 8.1 Verificar ejecución exitosa y generación de directorio.
    - [x] 8.2 Verificar contenido del manifiesto y archivos copiados.

- [x] 9. Agregar tiempo de ejecución a la salida de `build_cmi_portatil.py`.

0. Trabajando en la tarea: 10 :: 2026-01-21T12:40:00

- [x] 10. Crear Interfaz de Validacion Offline (apps/cmi_portatil/index.html).
    - [x] 10.1 Estructura HTML + CSS (Single File).
    - [x] 10.2 Lógica JS: Lectura de directorio y reporte de integridad.

0. Trabajando en la tarea: 11 :: 2026-01-21T12:55:00

- [x] 11. Implementar Frontend Seguro y Autosuficiente.
    - [x] 11.1 Configurar expiración y autoverificación.
    - [x] 11.2 Implementar listado y verificación on-demand (SHA-256).

0. Trabajando en la tarea: 12 :: 2026-01-21T13:20:00

- [x] 12. Refactorizar Pipeline de Construcción CMI (`build_cmi_portatil`).
    - [x] 12.1 Crear template Django `portable_index.html`.
    - [x] 12.2 Actualizar logica del comando (Template rendering, Zipping, Rotation).

0. Trabajando en la tarea: 13 :: 2026-01-21T14:05:00

- [x] 13. Refactorizar Frontend Portátil (CORS & WebkitDirectory).
    - [x] 13.1 Eliminar `fetch` y `showDirectoryPicker`.
    - [x] 13.2 Implementar mapeo de rutas con `webkitRelativePath`.
    - [x] 13.3 Auto-verificación en carga de carpeta.

0. Trabajando en la tarea: 14 :: 2026-01-21T14:50:00

- [x] 14. Refinamiento Final SGC Portátil (Autovalidación y Vigencia).
    - [x] 14.1 Validar cálculo de fechas y hash en `build_cmi_portatil`.
    - [x] 14.2 Ajustar mensajes y lógica crítica en `portable_index.html`.

0. Trabajando en la tarea: 15 :: 2026-01-21T15:30:00

- [x] 15. UI Animada y Gestión de Assets (Subfase A).
    - [x] 15.1 Copiar GIFs a carpeta assets/ en `build_cmi_portatil`.
    - [x] 15.2 Implementar modal de pasos (Scanning -> Fingerprint -> OK) en `portable_index`.








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

