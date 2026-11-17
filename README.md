# Portfolio — Agustín Cabral

Portfolio profesional bilingüe (español / inglés) para presentar experiencia laboral, formación, competencias y proyectos verificables de QA Automation, Data Analytics, desarrollo y automatización.

- **Sitio publicado:** https://portfolio.agustiincabral.workers.dev/
- **Repositorio:** https://github.com/agustiininicabral/html
- **Worker de Cloudflare:** `portfolio`
- **Rama principal:** `master`

## Identidad visual

- Azul hielo: `#F3F7F9`
- Bruma: `#E2EDF1`
- Azul profundo: `#142B3A`
- Turquesa: `#087E8B`
- Azul suave: `#9CBCC1`
- Terracota suave: `#C77D68`
- Naranja intenso (nombre en el Hero): `#FF4D00`

El Hero utiliza una fotografía de Mount Fuji de Alpsdake, publicada en Wikimedia Commons bajo CC BY-SA 4.0. El crédito y la licencia se muestran en el pie del sitio.

La primera visita permite elegir español o inglés. La preferencia se recuerda durante 3 horas y puede cambiarse desde el selector del encabezado.

## Estructura

- `index.html`: portfolio principal bilingüe.
- `style.css`: sistema visual responsive.
- `script.js`: selector ES/EN, preferencia de idioma, navegación activa y progreso de lectura.
- `cv.html`: CV en español, optimizado para impresión A4.
- `cv-en.html`: CV en inglés, optimizado para impresión A4.
- `assets/`: recursos visuales.
- `scripts/validate_site.py`: validaciones estructurales y de contenido.
- `wrangler.jsonc`: configuración de Cloudflare Workers Static Assets.
- `dist/`: copia de publicación; debe mantenerse sincronizada con los cinco archivos principales.

## Contenido

El portfolio distingue experiencia laboral, formación académica, cursos y proyectos personales. Los estudios universitarios incompletos no se presentan como títulos obtenidos. Los proyectos en desarrollo o pendientes de validación se identifican explícitamente.

### Proyectos destacados

1. Farmacia BI — proyecto de análisis y BI; los PBIX originales siguen pendientes de auditoría.
2. API Testing Framework — publicado.
3. Playwright UI Testing — publicado.
4. PriceWatch — aplicación local en desarrollo; integraciones reales con tiendas y notificaciones automáticas pendientes.
5. Automatic-OC — agente de escritorio local en desarrollo.
6. n8n Automation Portfolio — workflows educativos; importación y ejecución real pendientes de validación.
7. Excel to SQL — Users Migration — práctica de limpieza, deduplicación y carga de usuarios.
8. Excel to SQL — Roles & Permissions — práctica de modelado relacional y claves foráneas.
9. Excel to SQL — Activity History — práctica de auditoría, normalización UTC y validación de eventos.

Los tres proyectos Excel-to-SQL usan datos sintéticos, incluyen workbooks descargables, pruebas automatizadas y diagramas/resúmenes de validación; se presentan como práctica técnica.

## Desarrollo y validación

El sitio es estático: no requiere framework ni proceso de compilación. Los archivos fuente editables están en la raíz y `dist/` contiene la copia sincronizada que consume Cloudflare Workers Static Assets.

Después de modificar archivos fuente, sincronizá la copia publicada:

```bash
cp index.html style.css script.js cv.html cv-en.html dist/
```

Validación local:

```bash
python scripts/validate_site.py
node --check script.js
```

El validador comprueba que los cinco archivos de `dist/` existan y coincidan byte a byte con sus fuentes, además de revisar estructura HTML, enlaces internos, recursos locales, fechas laborales, proyectos, competencias, accesibilidad básica y configuración de despliegue.

## Despliegue

La configuración `wrangler.jsonc` define el nombre real del Worker como **`portfolio`** y publica el contenido de `dist/`. El sitio público es:

https://portfolio.agustiincabral.workers.dev/

El workflow de GitHub Actions:

- Valida la estructura y el contenido en cada pull request hacia `master`.
- Valida y comprueba la sintaxis de JavaScript en los pushes a `master`.
- En pushes a `master` y ejecuciones manuales, despliega con Wrangler 4 solo si están configurados los secretos `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID`.
- Si faltan credenciales, la validación puede finalizar correctamente, pero el despliegue se omite y se informa mediante una notificación.

Un push a `master` puede activar el workflow y, si los secretos están disponibles, publicar los cambios en producción. No se debe considerar un cambio desplegado hasta comprobar el resultado de la ejecución y el sitio público.

## Límites y transparencia

- Los proyectos con alcance parcial se etiquetan como tales.
- PriceWatch no consulta tiendas reales ni envía notificaciones automáticas.
- Automatic-OC continúa en desarrollo y no se presenta como producto terminado.
- Los workflows de n8n todavía requieren validación de importación y ejecución en una instancia real.
- Las competencias reúnen experiencia, formación y aplicación en proyectos; no implican dominio avanzado de cada herramienta.

© Agustín Cabral.
