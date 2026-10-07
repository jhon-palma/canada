"""Middleware propio del proyecto."""

from django.shortcuts import redirect

from apps.seo import (LANGUAGES, PORTADA_FRANCESA, PORTADAS_FRANCESAS,
                      SLUG_TRANSLATIONS)


class RevalidarHTML:
    """Pide al navegador que compruebe siempre si la pagina cambio.

    Django no manda ninguna cabecera de cache en las respuestas HTML: ni
    Cache-Control, ni Expires, ni Last-Modified, ni ETag. Sin esa informacion
    el navegador decide por su cuenta cuanto tiempo se queda con lo que tiene,
    y no hay manera barata de preguntarle al servidor si sigue vigente. De ahi
    que una ficha retirada, un articulo programado o un texto recien corregido
    pudieran seguir viendose durante un rato, y que la unica salida fuese una
    ventana de incognito.

    `no-cache` no significa "no lo guardes" -- eso es `no-store` --, sino
    "guardalo, pero pregunta antes de reutilizarlo". El navegador sigue
    conservando la pagina y su back/forward sigue siendo instantaneo; lo que
    ya no hace es darla por buena sin preguntar.

    Se probo acompanarlo de ConditionalGetMiddleware para que esa pregunta se
    resolviese con un 304 de unos pocos bytes en vez de reenviar la pagina, y
    no sirve aqui: el ETag sale del contenido, y el contenido cambia en cada
    render porque Django re-enmascara el token CSRF con sal aleatoria cada vez
    -- una defensa contra BREACH. Como el buscador de la cabecera pone un
    formulario en todas las paginas, dos renders identicos dan ETags
    distintos y el 304 no llega nunca. Habria costado un MD5 de 200 KB por
    peticion para no ahorrar nada.

    Se usa `private` porque la cabecera del sitio cambia segun haya sesion
    iniciada, asi que estas paginas no las puede compartir una cache
    intermedia entre visitantes distintos.

    Se deja intacta cualquier respuesta que ya declare su propia politica,
    como la vista previa de un articulo programado o lo que marque el admin.
    """

    CACHEABLE = frozenset(['GET', 'HEAD'])

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        respuesta = self.get_response(request)

        if request.method not in self.CACHEABLE:
            return respuesta
        if respuesta.has_header('Cache-Control'):
            return respuesta
        if not respuesta.get('Content-Type', '').startswith('text/html'):
            return respuesta

        respuesta['Cache-Control'] = 'private, no-cache'
        return respuesta


class RedirigirURLsMezcladas:
    """301 cuando el idioma de la URL no concuerda con el del slug.

    Los patrones de apps/web/urls.py aceptan el producto cartesiano de los dos
    segmentos: /en/propriete/<id>/detail/ responde 200 igual que
    /en/propertie/<id>/detail/, y lo mismo pasa con properties, acheter,
    vendre y el resto de la tabla. Son URLs distintas que devuelven byte a
    byte el mismo contenido, y Search Console las cuenta como duplicadas.

    Quien las fabricaba era el conmutador de idioma, que reescribia la URL en
    el navegador cambiando solo el segmento fr/en. Eso ya no ocurre, pero las
    que se generaron durante meses siguen en el indice y se siguen pidiendo,
    asi que hace falta decir que la buena es la otra. Un 301 lo dice y ademas
    traspasa la autoridad; dejarlas respondiendo 200 la reparte.

    Solo mira el segundo segmento de la ruta y solo contra una tabla en
    memoria: ninguna consulta. Las landings de busqueda tienen el mismo
    problema con los slugs de municipio y categoria, pero esos estan en la
    base y los resuelve SearchProperties, que ya los consulta de todos modos.
    """

    # slug -> (idioma al que pertenece, equivalente en el otro)
    PERTENENCIA = {}
    for _fr, _en in SLUG_TRANSLATIONS:
        PERTENENCIA[_fr] = ('fr', _en)
        PERTENENCIA[_en] = ('en', _fr)
    del _fr, _en

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        destino = self.ruta_corregida(request.path)
        if destino:
            consulta = request.META.get('QUERY_STRING')
            return redirect('{}?{}'.format(destino, consulta) if consulta else destino,
                            permanent=True)
        return self.get_response(request)

    @classmethod
    def ruta_corregida(cls, ruta):
        """La ruta canonica equivalente, o None si la pedida ya lo es."""
        # La portada francesa se sirve con el mismo HTML en / y en /fr/, y
        # Google tiene las dos indexadas repartiendose la autoridad. Cual es
        # la buena lo decide PORTADA_FRANCESA, de donde salen tambien el
        # canonical y el hreflang.
        if ruta in PORTADAS_FRANCESAS and ruta != PORTADA_FRANCESA:
            return PORTADA_FRANCESA

        partes = ruta.split('/')
        # ['', idioma, slug, ...]: hacen falta los dos primeros segmentos.
        if len(partes) < 3 or partes[1] not in LANGUAGES:
            return None
        idioma, slug = partes[1], partes[2]
        pertenencia = cls.PERTENENCIA.get(slug)
        if not pertenencia or pertenencia[0] == idioma:
            return None
        partes[2] = pertenencia[1]
        return '/'.join(partes)
