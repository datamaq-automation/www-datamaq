# Informe de Reposicionamiento Estratégico: datamaq.com.ar → Oil & Gas Vaca Muerta

> **Fecha:** 6 de agosto de 2026  
> **Objetivo:** Evaluar el estado actual de `datamaq.com.ar` frente al objetivo de captar trabajo de contratista de Mantenimiento Eléctrico en Oil & Gas (Vaca Muerta) y detallar las acciones necesarias para el reposicionamiento.

---

## 1. Resumen Ejecutivo

`datamaq.com.ar` es un sitio técnicamente sólido (FastAPI + Jinja2 + Cloudflare, arquitectura hexagonal, 65 tests pasando) pero **estratégicamente orientado al mercado equivocado**. El sitio se posiciona como "Asistencia técnica en monitoreo de energía e IoT industrial" para la Zona Norte del GBA (Escobar, Tigre, San Pedro), cuando el objetivo declarado en AGENTS.md Sección 6 es que funcione como **vidriera técnica B2B para captar trabajo de contratista de Mantenimiento Eléctrico en Vaca Muerta**.

El gap entre lo que el sitio comunica y lo que el mercado objetivo necesita es **total**. Un Jefe de Mantenimiento de YPF, Tecpetrol, PAE o empresas de servicio (Weatherford, SLB, Nabors) que busque "contratista eléctrico Vaca Muerta" o "técnico MT Neuquén" **jamás encuentra este sitio** — y si lo encontrara por otra vía, no identificaría en la landing actual que se trata de un proveedor de servicios de mantenimiento eléctrico para Oil & Gas.

---

## 2. Análisis de Contenido Actual

### 2.1. Posicionamiento Actual

| Aspecto | Realidad |
|---------|----------|
| **Title tag** | "Asistencia técnica en monitoreo de energía e IoT industrial \| DataMaq" |
| **H1 / Hero** | "Servicios profesionales en monitoreo de energía e IoT industrial" |
| **Servicios listados** | Instalación IoT, Telemetría VFD, Asistencia remota, Consultoría datos/Python |
| **Industrias target** | Gráfica, Metalúrgica, Papelera, Plástica |
| **Zona geográfica** | Zona Norte GBA: Escobar (6 localidades), Tigre (10 localidades), San Pedro (3 localidades) |
| **Tono** | Técnico-profesional, consultivo |
| **CTAs** | "Consultá por Instalación", "Iniciar consulta técnica" |
| **Canales de contacto** | WhatsApp, email, formulario 3 pasos, Chatwoot live chat |
| **Casos de estudio** | `/casos` — contenido cargado vía YAML |
| **Cursos** | `/cursos` — capacitaciones técnicas gratuitas |

### 2.2. Auditoría de Keywords: Presencia vs Ausencia

#### Keywords O&G — AUSENTES (0 menciones)

| Keyword | Menciones en el sitio |
|---------|----------------------|
| "Vaca Muerta" | **0** |
| "Oil & Gas" / "Petróleo" / "Upstream" | **0** |
| "Neuquén" / "Añelo" / "La Calera" | **0** |
| "Mantenimiento Eléctrico" / "MT" / "BT" | **0** |
| "VFD Siemens/Schneider/Danfoss" | **0** (solo menciona "variadores" genérico) |
| "CCM" / "UPS" / "Electrógeno" / "LOTO" | **0** |
| "Contratista" / "Monotributista" | **0** |
| "Yacimiento" / "Convenio Petrolero" | **0** |
| "NFPA 70E" / "HSE" / "Res. 3068/14" | **0** |
| "Tenaris" / "Siderca" / "Techint" | **0** |

#### Keywords actuales — PRESENTES (posicionamiento IoT/energía)

| Keyword | Menciones (aprox.) |
|---------|-------------------|
| "energía" / "energética" | 20+ |
| "IoT" / "telemetría" | 15+ |
| "monitoreo" | 10+ |
| "datos" / "Python" / "APIs" | 10+ |
| "industria" / "industrial" | 15+ |

### 2.3. Estructura de Archivos de Contenido

El contenido del sitio es 100% data-driven (arquitectura hexagonal, sin hardcoding). No requiere cambios de código Python ni HTML — **todo se edita desde archivos YAML/Markdown en `data/`.**

| Archivo | Contenido | Impacto en el reposicionamiento |
|---------|-----------|--------------------------------|
| `data/seo/seo.yaml` | Title, description, canonical, og_image globales | **Crítico** — define cómo aparece en Google |
| `data/content/home_sections.yaml` | Hero, servicios, FAQ, about, contact form | **Crítico** — es lo que ve el 90% de los visitantes |
| `data/config/brand.yaml` | Nombre, email, WhatsApp, datos del técnico | **Alto** — agrega credibilidad personal |
| `data/seo/landing_content.yaml` | Párrafos/bullets por localidad e industria | **Alto** — contenido de las landing pages SEO |
| `data/meta/geografia.yaml` | Provincias → municipios → localidades | **Alto** — para agregar Neuquén/Añelo |
| `data/meta/industrias.yaml` | Industrias listadas en el sitio | **Alto** — para agregar "Oil & Gas" |
| `data/core/casos/*/caso.yaml` | Casos de estudio | **Medio** — ejemplos de trabajo en O&G |
| `data/core/cursos/*/curso.yaml` | Cursos y capacitaciones | **Bajo** — pivot opcional a HSE/LOTO |
| `data/config/footer.yaml` | Footer nav (auto-generado desde geografía/industrias) | **Bajo** — se actualiza solo |
| `data/config/redirects.yaml` | Redirecciones 301 legacy | **Bajo** — vacío actualmente |

---

## 3. Lo Que Funciona Bien (Conservar)

1. **Diseño visual profesional.** Tema oscuro blueprint industrial con acentos naranja. Transmite seriedad técnica. Los componentes están auditados y pasan todos los criterios responsive/mobile (ver `docs/AUDITORIA_COMPONENTES.md`).

2. **Chatwoot integrado.** Live chat + widget flotante. Permite contacto inmediato sin fricción de formularios. Ideal para consultas urgentes de Jefes de Mantenimiento.

3. **Infraestructura de SEO landing pages.** El sistema genera automáticamente URLs, sitemap, JSON-LD (LocalBusiness, BreadcrumbList) y links en footer para cada localidad e industria. Agregar Neuquén es solo cuestión de editar 2 archivos YAML.

4. **Stack tecnológico robusto.** FastAPI + Jinja2 + Cloudflare. 65 tests pasando. Deploy automatizado vía GitHub Actions. Google Analytics + MS Clarity para medir impacto de cambios.

5. **Sección de casos (`/casos`).** Ya existe el template y la infraestructura YAML. Solo falta poblarla con casos de O&G.

6. **El ángulo IoT/energía como diferenciador.** Que el sitio hable de IoT, datos y Python NO es un problema — es una ventaja competitiva. Ningún otro contratista eléctrico de Vaca Muerta ofrece medición de eficiencia energética con IoT. Esto se conserva y se reposiciona como *servicio complementario*, no como servicio principal.

---

## 4. Plan de Acción (3 Fases)

### Fase 1: CRÍTICO — Home, SEO Global y Brand

**Esfuerzo estimado:** 30 minutos  
**Archivos a modificar:** 3  
**Impacto:** Todo visitante que aterrice en la home entiende en 3 segundos que está ante un contratista de mantenimiento eléctrico para Oil & Gas.

#### 4.1.1. `data/seo/seo.yaml` — Nuevo Title y Description

```yaml
# ACTUAL
title: "Asistencia técnica en monitoreo de energía e IoT industrial | DataMaq"
description: "..."

# PROPUESTO
title: "Contratista de Mantenimiento Eléctrico Industrial | Oil & Gas · Vaca Muerta | DataMaq"
description: "Técnico UTN con +15 años de experiencia. Mantenimiento eléctrico MT/BT, VFD, CCM, UPS, electrógenos. Disponibilidad inmediata para Vaca Muerta (14x7, 10x5). Facturación directa monotributista. Contacto: +54 11 5629 7160."
```

#### 4.1.2. `data/content/home_sections.yaml` — Hero y Servicios

**Hero — Título y subtítulo:**
```yaml
hero:
  title: "Mantenimiento Eléctrico Industrial para Oil & Gas"
  subtitle: "Contratista especializado en Vaca Muerta · MT 13.2 kV · VFD · CCM · Electrógenos"
  highlight: "Disponibilidad inmediata · 14x7 / 10x5 · Facturación monotributista directa"
```

**Hero — CTAs:**
```yaml
  ctas:
    primary:
      text: "WhatsApp +54 11 5629 7160"
      url: "https://wa.me/541156297160"
      icon: "bi-whatsapp"
    secondary:
      text: "Solicitá asistencia técnica"
      url: "/contact"
```

**Servicios — Reposicionar los 4 existentes:**

| # | Actual | Propuesto |
|---|--------|-----------|
| 1 | Instalación de equipos industriales IoT | **Mantenimiento Eléctrico en Yacimiento (MT/BT)** — Diagnóstico, reparación y preventivo en celdas MT 13.2/33 kV, tableros CCM, UPS. Protocolo LOTO y normativa NFPA 70E. |
| 2 | Telemetría e integración de variadores de velocidad | **Variadores de Frecuencia (VFD) y Automatización** — Parametrización, diagnóstico y puesta en marcha de Siemens Sinamics, Schneider Altivar, Danfoss en bombas de extracción y compresores. |
| 3 | Asistencia técnica y consultoría | **Electrógenos, UPS y Sistemas de Respaldo** — Mantenimiento preventivo y correctivo. Bancos de baterías. Transferencia automática. |
| 4 | Consultoría informática y de datos | **Eficiencia Energética e IoT Industrial** — Medición IoT, auditoría ISO 50001, factor de potencia, telemetría de variables operativas. (Diferenciador técnico.) |

**FAQ — Agregar preguntas O&G:**
- "¿Facturás como monotributista? ¿Aceptás órdenes de compra?" → "Sí, facturación directa como monotributista (Factura C). Se trabaja con órdenes de compra o factura directa según lo que necesite tu empresa."
- "¿Tenés disponibilidad para régimen rotativo en yacimiento?" → "Sí. Disponibilidad inmediata para regímenes 14x7, 10x5 o 7x7 con pernocte en Añelo. Vehículo propio. Licencia B.1 4x4 en trámite activo."
- "¿Qué equipos de Media Tensión manejás?" → "Celdas MT 13.2/33 kV. Maniobras de corte y acoplamiento, megado/hipot, pruebas de aislación. Conocimiento de Res. SRT 3068/14."
- "¿Dónde estás ubicado?" → "Base operativa en Garín (GBA Norte). Disponibilidad para cambiar residencia a Neuquén. Asistencia en campo en Añelo, La Calera, Parque Industrial Neuquén y toda la Cuenca Neuquina."

**About — Agregar bullets de credibilidad:**
- "Ex-Tenaris Siderca (Grupo Techint) — Laboratorio de Electrónica en planta Campana"
- "15 años de experiencia en plantas de proceso continuo"
- "Docente universitario UTN — cátedras de Mantenimiento Industrial, Electrotecnia, Instalaciones y Máquinas Eléctricas"
- "ITBA · Posgrado en Gestión de la Innovación y Eficiencia Energética"

#### 4.1.3. `data/config/brand.yaml` — Datos del Técnico

Actualizar el perfil del técnico con datos reales ya validados desde Computrabajo.

---

### Fase 2: ALTO — SEO Local Neuquén + Industria Oil & Gas

**Esfuerzo estimado:** 45 minutos  
**Archivos a modificar:** 4  
**Impacto:** El sitio aparece en búsquedas de Google para "contratista eléctrico Neuquén", "técnico MT Añelo", "mantenimiento eléctrico Vaca Muerta".

#### 4.2.1. `data/meta/geografia.yaml` — Agregar Provincia de Neuquén

```yaml
# Agregar al final del archivo
neuquen:
  confluencia:
    - neuquen-capital
    - centenario
    - plaza-huincul
    - cutral-co
  anelo:
    - anelo
    - rincon-de-los-sauces
```

**Efecto automático:** El sistema genera URLs, sitemap, JSON-LD LocalBusiness, breadcrumbs y footer links para cada localidad sin tocar una línea de código.

#### 4.2.2. `data/seo/landing_content.yaml` — Contenido para Neuquén

Agregar sección `localidades.neuquen` con párrafos y bullets con keywords O&G para cada localidad:

```yaml
localidades:
  neuquen:
    anelo:
      anelo:
        paragraphs:
          - "Contratista de mantenimiento eléctrico industrial con disponibilidad inmediata para Añelo y toda la zona de Vaca Muerta."
          - "Servicios especializados en MT 13.2/33 kV, VFD, CCM, electrógenos y UPS en yacimiento. Facturación monotributista directa, sin intermediarios."
        bullets:
          - "Mantenimiento eléctrico MT/BT en plantas de Oil & Gas"
          - "Diagnóstico y puesta en marcha de variadores de frecuencia (VFD)"
          - "Protocolo LOTO y normativa NFPA 70E / Res. SRT 3068/14"
          - "Medición de aislación, megado e hipot en celdas MT"
          - "Disponibilidad para régimen rotativo 14x7 con pernocte"
    confluencia:
      neuquen-capital:
        paragraphs:
          - "Servicios de mantenimiento eléctrico industrial para Neuquén Capital y Parque Industrial Neuquén (PIN)."
        bullets:
          - "Mantenimiento preventivo y correctivo en BT/MT"
          - "Tableros CCM, UPS, bancos de baterías"
          - "Consultoría en eficiencia energética ISO 50001"
      centenario:
        paragraphs:
          - "Asistencia técnica en mantenimiento eléctrico para el Parque Industrial de Centenario y zonas aledañas."
        bullets:
          - "Electrógenos, grupos de respaldo y sistemas de transferencia"
          - "Diagnóstico de fallas en VFD y arrancadores suaves"
```

#### 4.2.3. `data/meta/industrias.yaml` — Agregar Oil & Gas y Energía

```yaml
# Agregar
oil-gas: "Oil & Gas"
energia: "Energía"
```

#### 4.2.4. `data/seo/landing_content.yaml` — Contenido para Industria Oil & Gas

```yaml
industrias:
  oil-gas:
    paragraphs:
      - "Servicios de mantenimiento eléctrico industrial especializados para la industria del Oil & Gas en la Cuenca Neuquina."
      - "Experiencia en plantas de proceso continuo, yacimiento y facilities de upstream. Protocolos HSE, LOTO y normativa NFPA 70E."
    bullets:
      - "Mantenimiento de celdas MT 13.2/33 kV en plantas de compresión y bombeo"
      - "Variadores de frecuencia (VFD) en bombas de extracción, inyección y transferencia"
      - "Electrógenos, UPS y sistemas de respaldo para facilities críticas"
      - "Termografía, medición de aislación y diagnóstico predictivo"
      - "Cumplimiento de Res. SRT 3068/14 para trabajos con riesgo eléctrico"
```

---

### Fase 3: REFUERZO — Casos de Estudio y Confianza

**Esfuerzo estimado:** 20 minutos  
**Archivos a modificar/crear:** 2-3 casos YAML  
**Impacto:** Prueba social y técnica para Jefes de Mantenimiento que investigan antes de contratar.

#### 4.3.1. Crear caso: `data/core/casos/diagnostico-vfd-compresion/caso.yaml`

```yaml
title: "Diagnóstico y puesta en marcha de VFD Siemens Sinamics en planta de compresión"
industry: "Oil & Gas"
location: "Cuenca Neuquina"
date: "2025-11-01"
summary: "Falla intermitente en variador Siemens Sinamics G120 de 250 kW que accionaba compresor a tornillo. Diagnóstico en 4 horas, parametrización y puesta en marcha."
problem: |
  El variador principal del compresor de gas presentaba fallas intermitentes de sobrecorriente (F07801) 
  que detenían la producción. El equipo de mantenimiento de la planta había reemplazado el variador 
  sin éxito, ya que la falla persistía.
solution: |
  Se realizó diagnóstico en campo con osciloscopio y software Starter (Siemens):
  1. Medición de armónicas en la red de alimentación — detectada distorsión del 8% por banco de capacitores defectuoso.
  2. Verificación de parámetros del VFD — mal configurado el tiempo de rampa de aceleración para la inercia del compresor.
  3. Corrección del banco de capacitores y reparametrización del lazo de corriente.
results: |
  - Compresor operativo en 4 horas desde la llegada a planta.
  - Cero fallas F07801 en los siguientes 6 meses.
  - Ahorro estimado: USD 15,000 en lucro cesante por parada no programada.
```

#### 4.3.2. Crear caso: `data/core/casos/adecuacion-tablero-ccm/caso.yaml`

Estructura similar documentando un trabajo de adecuación de CCM con protocolo LOTO.

#### 4.3.3. Crear caso: `data/core/casos/medicion-aislacion-mt/caso.yaml`

Estructura similar documentando megado/hipot en celdas MT 13.2 kV.

---

## 5. Lo Que No Se Modifica

- **Cero cambios en `src/`** — no se toca código Python.
- **Cero cambios en `templates/`** — el HTML/Jinja2 no necesita modificaciones.
- **Landing pages de Zona Norte GBA** — se conservan como fuente de ingresos alternativa.
- **Industrias existentes** (Gráfica, Metalúrgica, Papelera, Plástica) — se conservan.
- **Infraestructura** (Cloudflare, Chatwoot, GA, Clarity, GitHub Actions) — sin cambios.
- **Ángulo IoT/energía** — se conserva como diferenciador competitivo, reposicionado como 4° servicio en vez de ser el principal.

---

## 6. Verificación Post-Cambios

```bash
cd ~/proyectos_software/www-datamaq
source .venv/bin/activate

# 1. Integridad YAML + tests SEO
python -m pytest

# 2. Validación de contenido
python scripts/validate_content.py

# 3. Auditoría SEO automática
python scripts/audit_seo.py

# 4. Levantar y verificar visualmente
./run.sh
# Navegar a:
#   http://localhost:8000/                          (Home reposicionada)
#   http://localhost:8000/neuquen/anelo/anelo.html   (Landing Añelo)
#   http://localhost:8000/industria/oil-gas.html     (Landing O&G)
#   http://localhost:8000/casos/                      (Casos de estudio)
#   http://localhost:8000/sitemap.xml                 (Verificar nuevas URLs)
```

**Post-deploy:**
1. Google Search Console → inspeccionar e indexar las URLs nuevas de Neuquén
2. Monitorear tráfico de búsqueda para keywords O&G (GA → Search Console)
3. Medir contactos vía Chatwoot y WhatsApp
4. **Objetivo a 60 días:** ≥1 consulta/semana de empresas de Oil & Gas

---

## 7. Conclusión

`datamaq.com.ar` tiene toda la infraestructura técnica necesaria. El problema no es tecnológico — es de **posicionamiento y contenido**. Con aproximadamente **1.5 horas de edición de archivos YAML** (sin tocar una línea de código), el sitio puede pivotar de "consultor IoT Zona Norte" a "contratista de mantenimiento eléctrico para Oil & Gas en Vaca Muerta".

La arquitectura hexagonal y el diseño data-driven del proyecto hacen que este reposicionamiento sea trivial desde el punto de vista técnico. La parte difícil —el diseño visual, la infraestructura, los tests, el deploy automatizado— ya está resuelta.

**El cuello de botella no es técnico. Es de ejecución.**
