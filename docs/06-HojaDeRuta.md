# Hoja de Ruta - Refactorización y Mejoras

Este documento rastrea el progreso de las tareas de refactorización y desarrollo.

0. Trabajando en la tarea: 3 :: 2024-12-11

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
