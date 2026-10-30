# Portfolio — Agustín Cabral

Sitio profesional estático para presentar experiencia, habilidades y proyectos de Data Analytics, Data Quality, QA y automatización.

## Archivos

- `index.html`: contenido principal, versión ES/EN.
- `style.css`: estilos responsive y sistema visual azul marino/cian.
- `script.js`: navegación, idioma y efectos de interfaz.
- `cv.html`: CV imprimible desde el navegador.

## Validaciones

El workflow de GitHub Actions comprueba la estructura HTML, los destinos de navegación, los ocho proyectos, los archivos locales y la sintaxis JavaScript antes de desplegar.

## Despliegue en Cloudflare Workers

El sitio se publica como Static Assets en el Worker `portfolio-agustin`.

Configurar una sola vez en GitHub: **Settings → Secrets and variables → Actions → New repository secret**.

- `CLOUDFLARE_API_TOKEN`: token de Cloudflare con permisos para editar Workers Scripts en la cuenta.
- `CLOUDFLARE_ACCOUNT_ID`: ID de la cuenta Cloudflare.

No guardar tokens en archivos del repositorio, código, commits ni logs.

Cada push a `master` que modifique archivos del sitio ejecuta validaciones y, si pasan, publica el sitio. También se puede iniciar manualmente desde **Actions → Validate and deploy portfolio → Run workflow**.
