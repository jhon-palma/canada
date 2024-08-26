from apps.properties.models import Municipalites

municipalites = Municipalites.objects.filter(slug_francaise__isnull=True) | Municipalites.objects.filter(slug_anglaise__isnull=True)

for municip in municipalites:
    municip.save()
    print(f"Updated {municip.code}: slug_francaise={municip.slug_francaise}, slug_anglaise={municip.slug_anglaise}")


from apps.properties.models import GenresProprietes

# genres = GenresProprietes.objects.filter(slug_francaise__isnull=True) | GenresProprietes.objects.filter(slug_anglaise__isnull=True)
genres = GenresProprietes.objects.all()

for genre in genres:
    genre.save()
    print(f"Updated {genre.genre_propriete}: slug_francaise={genre.slug_francaise}, slug_anglaise={genre.slug_anglaise}")