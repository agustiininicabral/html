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

El sitio es estático y no requiere framework ni framework de compilación. Los archivos fuente editables están en la raíz y la carpeta dist/ contiene una copia sincronizada lista para el despliegue directo desde Cloudflare.

Para actualizar la carpeta publicada después de editar los archivos fuente:

    mkdir -p dist
    cp index.html style.css script.js cv.html cv-en.html dist/

Validación local:

    python scripts/validate_site.py
    node --check script.js

La validación comprueba que los cinco archivos de dist/ existan y coincidan byte a byte con sus fuentes.

## Despliegue

El proyecto se publica como Static Assets en el Worker portfolio-agustin.

El workflow de GitHub Actions valida el contenido, prepara los archivos en dist/ y despliega mediante Wrangler 4 cuando están configurados los secretos CLOUDFLARE_API_TOKEN y CLOUDFLARE_ACCOUNT_ID.

El repositorio es agustiininicabral/html y el Worker de destino es portfolio-agustin. La configuración wrangler.jsonc conserva el nombre del Worker y apunta a dist/. La carpeta dist/ está versionada para que una compilación Git-connected de Cloudflare pueda ejecutar npx wrangler deploy sin depender de un paso previo de generación.

## Límites y transparencia

- Los proyectos con alcance parcial se etiquetan como tales.
- PriceWatch no consulta tiendas reales ni envía notificaciones automáticas.
- Automatic-OC continúa en desarrollo y no se presenta como producto terminado.
- Los workflows de n8n todavía requieren validación de importación y ejecución en una instancia real.
- Las competencias reúnen experiencia, formación y aplicación en proyectos; no implican dominio avanzado de cada herramienta.

© Agustín Cabral.
