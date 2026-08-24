"""Middleware propio del proyecto."""


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
