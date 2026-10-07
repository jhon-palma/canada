"""Aplica los textos y las correcciones de contenido de la revision de SEO.

Son cambios en la base, no en el codigo: los titulos y descripciones de
web_metadata, tres titulos de articulo que estaban en ingles en el campo
frances, y los siete articulos de relleno que estan publicados.

Va como comando y no aplicado a mano por tres razones. La base de produccion
no es la del entorno de desarrollo, asi que esto tiene que ejecutarse alli y
no aqui. Es repetible: si se ejecuta dos veces la segunda no hace nada, y si
el despliegue se repite tampoco. Y queda en el repositorio, de modo que dentro
de seis meses se puede leer que se cambio y por que, que es mas de lo que
queda de una edicion hecha a mano en un formulario.

Sin argumentos solo informa de lo que haria. Para escribir hay que pedirlo:

    manage.py aplicar_textos_seo            # muestra el plan
    manage.py aplicar_textos_seo --aplicar  # lo ejecuta
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.blog.models import Article
from apps.web.models import MetaDataWeb


# Una fila por pagina. De las diez, ocho tenian el titulo ingles metido en el
# campo frances y cinco repetian la misma cadena generica en los dos idiomas,
# asi que media docena de paginas compartia titulo. Los de 'index' son los que
# propone la revision de Search Console; el resto siguen su linea.
METADATOS = {
    'index': (
        "Courtiers immobiliers à Montréal | Acheter, vendre, investir | LJ Immobilier",
        "Montreal Real Estate Brokers | Buy, Sell & Invest | LJ Realties",
        "Plus de 945 ventes et plus de 610 M$ en volume. LJ Immobilier vous accompagne pour acheter, vendre ou investir à Montréal et dans le Sud-Ouest.",
        "Over 945 sales and more than $610M in volume. LJ Realties helps you buy, sell or invest in Montreal and the Sud-Ouest.",
    ),
    'properties': (
        "Propriétés à vendre et à louer à Montréal | LJ Realties",
        "Properties for Sale and Rent in Montreal | LJ Realties",
        "Maisons, condos et plex à vendre et à louer à Montréal. Photos, prix et visites avec les courtiers de LJ Realties.",
        "Houses, condos and plexes for sale and rent in Montreal. Photos, prices and viewings with the brokers at LJ Realties.",
    ),
    'sale': (
        "Propriétés à vendre à Montréal et au Sud-Ouest | LJ Realties",
        "Properties for Sale in Montreal and the Sud-Ouest | LJ Realties",
        "Toutes nos propriétés à vendre à Montréal et au Sud-Ouest, mises à jour chaque jour. Prix, photos et visites avec LJ Realties.",
        "Every property we have for sale in Montreal and the Sud-Ouest, updated daily. Prices, photos and viewings with LJ Realties.",
    ),
    'rent': (
        "Propriétés à louer à Montréal | LJ Realties",
        "Properties for Rent in Montreal | LJ Realties",
        "Appartements, condos et maisons à louer à Montréal. Disponibilités à jour et visites avec les courtiers de LJ Realties.",
        "Apartments, condos and houses for rent in Montreal. Current availability and viewings with the brokers at LJ Realties.",
    ),
    'buy': (
        "Acheter une propriété à Montréal | Accompagnement complet | LJ Realties",
        "Buying a Property in Montreal | Full Guidance | LJ Realties",
        "De la recherche à la signature : financement, visites, négociation et vérifications. Consultation d'acheteurs gratuite avec LJ Realties.",
        "From search to signing: financing, viewings, negotiation and verifications. Free buyers consultation with LJ Realties.",
    ),
    'sell': (
        "Vendre ma maison à Montréal | Évaluation gratuite | LJ Realties",
        "Sell My House in Montreal | Free Evaluation | LJ Realties",
        "En 2025 nous avons vendu 41% plus vite que la moyenne à Montréal. Obtenez l'évaluation gratuite de votre propriété avec LJ Realties.",
        "In 2025 we sold 41% faster than the Montreal average. Get a free evaluation of your property with LJ Realties.",
    ),
    'team': (
        "Nos courtiers immobiliers à Montréal | LJ Realties",
        "Our Real Estate Brokers in Montreal | LJ Realties",
        "Rencontrez les courtiers de LJ Realties : plus de 945 transactions dans le Sud-Ouest, Ville-Marie et le Grand Montréal.",
        "Meet the brokers at LJ Realties: over 945 transactions across the Sud-Ouest, Ville-Marie and Greater Montreal.",
    ),
    'contact': (
        "Nous joindre | Courtiers immobiliers à Montréal | LJ Realties",
        "Contact Us | Real Estate Brokers in Montreal | LJ Realties",
        "Parlez à un courtier de LJ Realties. 1117 rue Charlevoix, Montréal. Téléphone, courriel et formulaire de contact.",
        "Talk to a broker at LJ Realties. 1117 rue Charlevoix, Montreal. Phone, email and contact form.",
    ),
    'blog': (
        "Blogue immobilier Montréal | Conseils d'achat et de vente | LJ Realties",
        "Montreal Real Estate Blog | Buying and Selling Advice | LJ Realties",
        "Taxe de bienvenue, budget d'achat, augmentations de loyer : ce qu'il faut savoir avant d'acheter ou de vendre à Montréal.",
        "Welcome tax, purchase budgets, rent increases: what to know before buying or selling in Montreal.",
    ),
    'video': (
        "Vidéos immobilières Montréal | LJ Realties",
        "Montreal Real Estate Videos | LJ Realties",
        "Visites de propriétés, chroniques CJAD et conseils en vidéo par les courtiers de LJ Realties à Montréal.",
        "Property tours, CJAD segments and video advice from the LJ Realties brokers in Montreal.",
    ),
}


# Articulos cuyo titulo frances estaba en ingles. Se identifican por el slug
# frances, que no se toca: cambiarlo cambiaria la URL y esas ya estan
# indexadas. Que dos de esos slugs lleven mayusculas es otra cosa, y tampoco
# se arregla aqui por el mismo motivo.
TITULOS_FRANCESES = {
    'is-it-better-to-buy-or-rent-in-montreal-right-now':
        "Vaut-il mieux acheter ou louer à Montréal en ce moment ?",
    'should-I-buy-a-condo-house-or-plex-in-Montreal':
        "Condo, maison ou plex : qu'acheter à Montréal ?",
    'bank-of-canada-announcement-June-2025':
        "La Banque du Canada maintient son taux : ce que cela signifie pour le marché immobilier",
}


# Articulos de relleno publicados: su contenido es su propio titulo. Se
# desactivan en vez de borrarse, que es reversible desde el formulario de
# siempre. Se comprueba tambien el titulo antes de tocar nada, por si en
# produccion esos slugs fueran de otra cosa.
RELLENO = ['pendiente-%d' % n for n in range(1, 8)]


class Command(BaseCommand):
    help = 'Aplica los textos y las correcciones de contenido de la revision de SEO.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--aplicar', action='store_true',
            help='Escribe los cambios. Sin esta opcion solo se informa de lo que haria.')

    def handle(self, *args, **opciones):
        aplicar = opciones['aplicar']
        if not aplicar:
            self.stdout.write(self.style.WARNING(
                'Simulacion: no se escribe nada. Anade --aplicar para ejecutarlo.\n'))

        with transaction.atomic():
            cambios = (self._metadatos(aplicar)
                       + self._titulos(aplicar)
                       + self._relleno(aplicar))
            if not aplicar:
                transaction.set_rollback(True)

        self.stdout.write('')
        if cambios:
            verbo = 'Aplicados' if aplicar else 'Pendientes de aplicar'
            self.stdout.write(self.style.SUCCESS('%s %d cambios.' % (verbo, cambios)))
        else:
            self.stdout.write(self.style.SUCCESS('Nada que cambiar: ya esta todo puesto.'))

    # ------------------------------------------------------------------ partes

    def _metadatos(self, aplicar):
        self.stdout.write(self.style.MIGRATE_HEADING('Titulos y descripciones de las paginas'))
        cambios = 0
        for origin, (titulo_f, titulo_a, descr_f, descr_a) in METADATOS.items():
            fila = MetaDataWeb.objects.filter(origin=origin).first()
            if fila is None:
                fila = MetaDataWeb(origin=origin)
                nueva = True
            else:
                nueva = False

            actual = (fila.m_title_f, fila.m_title_a, fila.m_description_f, fila.m_description_a)
            if actual == (titulo_f, titulo_a, descr_f, descr_a):
                self.stdout.write('  = %-12s ya esta puesto' % origin)
                continue

            fila.m_title_f, fila.m_title_a = titulo_f, titulo_a
            fila.m_description_f, fila.m_description_a = descr_f, descr_a
            if aplicar:
                fila.save()
            self.stdout.write('  %s %-12s %s' % (
                '+' if nueva else 'v', origin, 'fila nueva' if nueva else 'actualizada'))
            cambios += 1
        return cambios

    def _titulos(self, aplicar):
        self.stdout.write(self.style.MIGRATE_HEADING('Titulos de articulo que estaban en ingles'))
        cambios = 0
        for slug, titulo in TITULOS_FRANCESES.items():
            articulo = Article.objects.filter(slug_francaise=slug).first()
            if articulo is None:
                self.stdout.write(self.style.WARNING('  ? %s no existe en esta base' % slug))
                continue
            if articulo.title_francaise == titulo:
                self.stdout.write('  = %s ya esta en frances' % slug)
                continue
            articulo.title_francaise = titulo
            if aplicar:
                articulo.save(update_fields=['title_francaise'])
            self.stdout.write('  v %s' % slug)
            self.stdout.write('      %s' % titulo)
            cambios += 1
        return cambios

    def _relleno(self, aplicar):
        self.stdout.write(self.style.MIGRATE_HEADING('Articulos de relleno publicados'))
        cambios = 0
        for slug in RELLENO:
            articulo = Article.objects.filter(slug_francaise=slug).first()
            if articulo is None:
                self.stdout.write(self.style.WARNING('  ? %s no existe en esta base' % slug))
                continue
            # El titulo se comprueba antes de desactivar: si en produccion ese
            # slug fuera de un articulo de verdad, no se toca.
            if not (articulo.title_francaise or '').strip().lower().startswith('pendiente'):
                self.stdout.write(self.style.WARNING(
                    '  ! %s no parece de relleno ("%s"): se deja como esta'
                    % (slug, articulo.title_francaise)))
                continue
            if not articulo.active:
                self.stdout.write('  = %s ya esta desactivado' % slug)
                continue
            articulo.active = False
            if aplicar:
                articulo.save(update_fields=['active'])
            self.stdout.write('  v %s desactivado' % slug)
            cambios += 1
        return cambios
