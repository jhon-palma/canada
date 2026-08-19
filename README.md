## canada

Sitio de LJ Realties (Django).

## Despliegue de estaticos

Los CSS y JS del sitio viven en `static/` y se **sirven desde Spaces**, no
desde el servidor: el navegador los pide al edge del CDN
(`media-canada.sfo3.cdn.digitaloceanspaces.com`). Un `git pull` en el servidor
deja los archivos en disco pero **no los publica**: hasta que no se suben al
bucket, la pagina los recibe con 404.

Tras editar cualquier CSS o JS, en el servidor y con `DEBUG=False`:

```bash
python manage.py publish_static
```

Encadena los tres pasos y aborta en cuanto uno falla:

1. `build_bundles` — regenera `web/css/bundle.css` y `web/js/bundle.js` a
   partir de los 9 CSS y 2 JS que carga el header.
2. `collectstatic` — sube a Spaces con ACL `public-read`.
3. Descarga las URLs publicas y compara el sha1 con el archivo local.

El tercer paso es el que importa: los dos primeros pueden terminar sin error y
dejar el sitio roto igualmente. Para comprobar el estado sin subir nada, desde
cualquier maquina:

```bash
python manage.py publish_static --check
python manage.py publish_static --check --verificar web/css/master.css
```

### Comandos relacionados

- `build_bundles --check` — avisa si los bundles del repositorio no reflejan
  sus archivos de origen. Conviene ejecutarlo antes de un commit que toque
  CSS o JS del header.
- `fix_static_acl --apply` — devuelve a `public-read` los objetos del bucket
  que quedaron privados. Sin eso, django-storages recurre a URLs firmadas, que
  caducan y no se pueden cachear.
