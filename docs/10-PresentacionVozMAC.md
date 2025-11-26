# Guión de Presentación Comercial: VozMAC

| Documento | Presentación comercial (guión) |
| ----: | :---- |
| **Versión** | 1.0 |
| **Fecha** | 09 de octubre de 2025 |
| **Dirigido a** | Titulares de la Junta Local del INE Tlaxcala, Vocalías distritales y aliados estratégicos |

---

## Pantalla 1. Portada
- **Mensaje central:** "VozMAC: Transformando la voz ciudadana en decisiones de calidad".
- **Elementos visuales sugeridos:** logotipo INE, logotipo VozMAC, fotografía de un MAC en operación.
- **Narrativa:** "Bienvenidas y bienvenidos. Hoy presentamos VozMAC, la nueva plataforma que coloca la opinión ciudadana en el centro de la gestión de calidad en los Módulos de Atención Ciudadana".

## Pantalla 2. Problema Actual
- **Título:** "Situación actual: procesos manuales, respuestas tardías".
- **Puntos clave:**
  - Captura en papel implica retrasos, costos y riesgos de transcripción.
  - La información llega tarde a las Vocalías; se actúa de manera reactiva.
  - El ciudadano no percibe retroalimentación directa.
- **Narrativa:** Explicar cómo estos puntos derivan en oportunidades perdidas para mejorar el servicio.

## Pantalla 3. Oportunidad Estratégica
- **Título:** "Del dato manual a la inteligencia operativa".
- **Puntos clave:**
  - Digitalizar la encuesta de satisfacción.
  - Integrar con el Sistema de Gestión de la Calidad (SGC) para análisis inmediato.
  - Crear un ciclo virtuoso de mejora continua.
- **Narrativa:** "La voz ciudadana deja de ser un registro histórico y se convierte en insumo diario para decisiones".

## Pantalla 4. Qué es VozMAC
- **Título:** "VozMAC en una frase".
- **Mensaje:** "Aplicación móvil + flujo de exportación seguro que captura y entrega la satisfacción ciudadana en tiempo casi real".
- **Elementos visuales:** mockups de pantalla encuesta y panel operador.
- **Narrativa:** Resaltar que es el primer eslabón del ciclo de retroalimentación automatizado.

## Pantalla 5. Flujo del Ciudadano
- **Título:** "Experiencia simplificada en 3 pasos".
- **Pasos:**
  1. Selección de tipo de visita.
  2. Contestación de encuesta con botones intuitivos.
  3. Mensaje de agradecimiento y reinicio automático.
- **Narrativa:** Enfatizar accesibilidad, rapidez y consistencia visual.

## Pantalla 6. Flujo del Operador
- **Título:** "Panel de control para el MAC".
- **Puntos clave:**
  - Conteo en tiempo real de encuestas por exportar.
  - Exportación en formato NDJSON comprimido (.gz) mediante SAF.
  - Botón de edición de configuración con trazabilidad.
- **Narrativa:** "El operador no depende de TI para capturar o extraer datos".

## Pantalla 7. Seguridad y Cumplimiento
- **Título:** "Protección de datos y control transaccional".
- **Puntos clave:**
  - Almacenamiento local cifrado (Room + encriptación de dispositivo).
  - Exportación validada con hash SHA-256 y cambio de estado is_exported solo tras confirmación exitosa.
  - Uso del Storage Access Framework para cumplir lineamientos de seguridad.
- **Narrativa:** Referenciar políticas INE y auditorías del SGC.

## Pantalla 8. Distribución Piloto 2025
- **Título:** "Plan de despliegue en Tlaxcala".
- **Puntos clave:**
  - MAC involucrados (Apizaco, Chiautempan, Huamantla, Tlaxcala).
  - Entrega controlada con kits cifrados y manuales.
  - Calendario de instalación y acompañamiento.
- **Narrativa:** Alinear con la estrategia de distribución aprobada.

## Pantalla 9. Beneficios Tangibles
- **Título:** "Impacto directo para stakeholders".
- **Para la Vocalía:** visibilidad diaria, decisiones basadas en evidencia.
- **Para el MAC:** reducción de carga operativa, foco en servicio.
- **Para la ciudadanía:** percepción de respuesta inmediata y transparencia.
- **Narrativa:** Incorporar testimonios proyectados o resultados esperados.

## Pantalla 10. Métricas de Éxito
- **Título:** "Cómo mediremos el valor".
- **Indicadores sugeridos:**
  - Tasa de respuesta >75% en cada MAC.
  - Tiempo de exportación <5 minutos por jornada.
  - Encuestas calificadas listadas en el SGC antes de 24 h.
  - Satisfacción interna del personal >90%.
- **Narrativa:** "Los indicadores conectan VozMAC con la mejora continua del SGC".

## Pantalla 11. Roadmap a Futuro
- **Título:** "Escalamiento 2026 y más allá".
- **Etapas:**
  - Integración API con SGC central.
  - Panel analítico para Vocalías distritales.
  - Escalamiento gradual a nivel nacional.
- **Narrativa:** "El MVP es el punto de partida".

## Pantalla 12. Llamado a la Acción
- **Título:** "Activemos VozMAC".
- **Puntos:**
  - Aprobar el plan de distribución.
  - Designar responsables de instalación y seguimiento.
  - Calendarizar evaluaciones bimestrales de resultados.
- **Narrativa:** Cerrar con invitación a sumarse y con la frase "La voz ciudadana se escucha mejor cuando se gestiona con evidencia".

---

**Notas para el presentador:**
- Mantener la sesión en 20 minutos con espacio para preguntas.
- Traer dispositivo demo con APK `vozmac-v1.1-release.apk` instalado.
- Llevar un reporte de exportación generado con el flujo productivo para mostrar la estructura NDJSON.
- Preparar sección Q&A frecuente: seguridad, soporte y escalabilidad.
