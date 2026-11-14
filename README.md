# Portfolio — Agustín Cabral

Portfolio profesional bilingüe (español / inglés) para presentar experiencia laboral, formación, competencias y proyectos verificables de QA Automation, Data Analytics, desarrollo y automatización.

Sitio: https://portfolio-agustin.agustinkbral2013.workers.dev/

## Identidad visual

- Marfil: #F5F1E9
- Arena: #E5DED2
- Carbón: #252525
- Terracota: #A65D42
- Beige: #B9A58D

El Hero utiliza una fotografía de Mount Fuji de Alpsdake, publicada en Wikimedia Commons bajo CC BY-SA 4.0. Se aplica un tratamiento visual tenue y cálido. Crédito y licencia visibles en el pie del sitio.

## Estructura

- index.html: portfolio principal bilingüe.
- style.css: sistema visual editorial y responsive.
- script.js: selector ES/EN, preferencia de idioma, navegación activa y progreso de lectura.
- cv.html: CV en español, optimizado para impresión A4.
- cv-en.html: CV en inglés, optimizado para impresión A4.
- scripts/validate_site.py: validaciones estructurales y de contenido.
- wrangler.jsonc: configuración de Cloudflare Workers Static Assets.

## Contenido

El portfolio distingue experiencia laboral, formación académica, cursos y proyectos personales. Los estudios universitarios incompletos no se presentan como títulos obtenidos. Los proyectos en desarrollo o pendientes de validación se identifican explícitamente.

### Proyectos destacados

1. API Testing Framework — publicado.
2. Playwright UI Testing — publicado.
3. PriceWatch — aplicación local en desarrollo; integraciones reales con tiendas y notificaciones automáticas pendientes.
4. Automatic-OC — agente de escritorio local en desarrollo.
5. n8n Automation Portfolio — workflows educativos; importación y ejecución real pendientes de validación.

## Desarrollo y validación

El sitio es estático y no requiere framework ni proceso de compilación.

    python scripts/validate_site.py
    node --check script.js

## Despliegue

El proyecto se publica como Static Assets en el Worker portfolio-agustin.

El workflow de GitHub Actions valida el contenido, prepara los archivos en dist/ y despliega mediante Wrangler 4 cuando están configurados los secretos CLOUDFLARE_API_TOKEN y CLOUDFLARE_ACCOUNT_ID.

Los cambios de rediseño se preparan en una rama independiente. No integrar a master ni publicar en producción hasta completar la revisión visual, funcional y de contenido.

## Límites y transparencia

- Los proyectos con alcance parcial se etiquetan como tales.
- PriceWatch no consulta tiendas reales ni envía notificaciones automáticas.
- Automatic-OC continúa en desarrollo y no se presenta como producto terminado.
- Los workflows de n8n todavía requieren validación de importación y ejecución en una instancia real.
- Las competencias reúnen experiencia, formación y aplicación en proyectos; no implican dominio avanzado de cada herramienta.

© Agustín Cabral.
