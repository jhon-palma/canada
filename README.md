## canada

Sitio de LJ Realties (Django).

## Desplegar

```bash
cd /home/doadmin/canada
git pull
python3 manage.py migrate          # solo si el cambio trae migraciones
pkill -HUP -f 'gunicorn immobilier.wsgi'
```

### Reiniciar la aplicacion

**`systemctl restart gunicorn` no sirve: no hay ninguna unidad de systemd.**
La aplicacion la sirve gunicorn arrancado por fuera, como el usuario `doadmin`
y escuchando en un socket unix, y nginx le hace `proxy_pass`:

```
gunicorn immobilier.wsgi:application --name canada --workers 3
         --bind=unix:/home/doadmin/run/gunicorn.sock
```

Para que tome el codigo nuevo se le manda HUP al proceso maestro, que recarga
los workers sin cortar peticiones:

```bash
pkill -HUP -f 'gunicorn immobilier.wsgi'
```

Sin ese paso el `git pull` no cambia nada: los workers siguen con el codigo
que tenian en memoria.

### La cache de Cloudflare

El sitio esta detras de Cloudflare, y si hay una regla que cachea HTML
(*Cache Everything* en Page Rules o en Cache Rules) el navegador sigue viendo
la version anterior aunque el origen ya responda otra cosa. Para saber que
esta contestando de verdad el servidor, saltandose Cloudflare:

```bash
curl -sk --resolve www.ljrealties.com:443:127.0.0.1   -o /dev/null -w "origen -> %{http_code}
"   "https://www.ljrealties.com/fr/blog/<slug>/"
```

Si el origen y el navegador no coinciden, la diferencia es la cache: se purga
en Caching -> Configuration -> Purge Everything.

Cachear HTML choca con la publicacion programada del blog en las dos
direcciones: un articulo retirado sigue visible hasta que caduque la cache, y
uno programado sigue dando 404 despues de su hora de salida. Lo segundo es
peor porque no se nota. Conviene dejar el HTML fuera de la cache del edge; los
estaticos, que son el peso real, ya vienen del CDN de Spaces.

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
2. `sync_static` — sube a Spaces lo que haya cambiado, con ACL `public-read`.
3. Descarga las URLs publicas y compara el sha1 con el archivo local.

Con todo al dia tarda unos segundos. Para ensayarlo sin escribir nada en el
bucket, `publish_static --dry-run`.

El tercer paso es el que importa: los dos primeros pueden terminar sin error y
dejar el sitio roto igualmente. Para comprobar el estado sin subir nada, desde
cualquier maquina:

```bash
python manage.py publish_static --check
python manage.py publish_static --check --verificar web/css/master.css
```

### Por que no collectstatic

`collectstatic` funciona, pero tarda varios minutos aunque no haya nada que
subir. Decide archivo a archivo: por cada uno de los 2142 hace dos peticiones
a Spaces en serie —¿existe?, ¿de que fecha es?— y espera la respuesta antes
de pasar al siguiente. Son 4284 viajes de ida y vuelta a San Francisco, en un
solo hilo.

`sync_static` pide el inventario del bucket de una vez (`list_objects_v2`
devuelve 1000 objetos por peticion, con su tamano y su ETag: 4 llamadas en
lugar de 4284) y sube en paralelo lo que difiera. Ademas compara **contenido**
y no fechas: el ETag de un objeto subido de una pieza es su MD5, asi que
tambien detecta un archivo que en el bucket este cambiado pero con fecha
posterior, cosa que collectstatic no ve nunca.

Respeta los mismos patrones que ignora collectstatic (`CVS`, `.*`, `*~`), asi
que no sube los `.DS_Store`.

### Comandos relacionados

- `build_bundles --check` — avisa si los bundles del repositorio no reflejan
  sus archivos de origen. Conviene ejecutarlo antes de un commit que toque
  CSS o JS del header.
- `fix_static_acl --apply` — devuelve a `public-read` los objetos del bucket
  que quedaron privados. Sin eso, django-storages recurre a URLs firmadas, que
  caducan y no se pueden cachear.

## La base de datos de desarrollo

Desarrollar contra una base vacia esconde la mitad de los problemas: las
fichas reales traen campos a medias, barrios con tildes y cientos de
propiedades donde el entorno limpio tiene tres. `clonar_db_produccion` trae
una copia de produccion y la restaura encima de la base local.

```bash
python manage.py clonar_db_produccion            # muestra el plan, no escribe
python manage.py clonar_db_produccion --aplicar  # vuelca y restaura
```

El origen sale de `.env.prod` y el destino de la configuracion cargada. Antes
de tocar nada comprueba que el destino esta en esta maquina y que no coincide
con el origen, porque el primer paso de la restauracion es destruir el esquema
`public`: con un `DJANGO_ENV=prod` de mas, lo que se borraria es produccion.

La base de DigitalOcean solo admite las IP que figuran en Trusted Sources, asi
que desde una maquina de casa el volcado no conecta. O se anade la IP en el
panel, o se parte en dos:

```bash
# en el servidor
python manage.py clonar_db_produccion --aplicar --solo-descargar
# en la maquina de desarrollo, con el archivo ya copiado
python manage.py clonar_db_produccion --aplicar --desde data/backups/produccion-....dump
```

Usa `pg_dump` y `pg_restore`, no `dumpdata`/`loaddata`: estos pasan por el ORM,
tardan muchisimo mas, se atragantan con las referencias circulares y no
reproducen secuencias ni indices. Si el cliente de PostgreSQL no esta en el
PATH —lo normal en Windows— se busca en `C:/Program Files/PostgreSQL/*/bin`,
o se indica con `--pg-bin`.

El volcado queda en `data/backups/`, que no se versiona. **Contiene los datos
reales de los clientes**: correos, telefonos y hashes de contrasena. No sale de
la maquina y se borra cuando deja de hacer falta.
