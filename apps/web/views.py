import pdb
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.contrib import auth,messages
from django.core.paginator import Paginator
from django.db.models import Value, CharField, Q
from django.template.loader import *
from django.urls import reverse
from django.views.decorators.csrf import *
from django.views.generic import *
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Value, IntegerField

from datetime import *
from apps.users.models import Profile
from apps.web.models import *
from apps.web.forms import *
from ..properties.models import *
from ..labels import DICT_LABELS
from googleapiclient.discovery import build
from django.utils.dateparse import parse_datetime



class WebCalculator(TemplateView):
    template_name = 'web/calculator.html'


class WebIndex(View):
    template_name = 'web/index.html'
    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        data_meta = MetaDataWeb.objects.get(origin='index')
        inscriptions = Inscriptions.objects.filter(prix_demande__isnull=False, status=True).exclude(code_statut__valeur="VE").annotate(
            usa_last=Case(
                When(mun_code__description__icontains="USA", then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField() 
            )
        ).order_by('usa_last', '-no_inscription')[:3]
        staticts_query = Statistics.objects.all()
        images_query = ImagesWeb.objects.filter(reference__in=[
            'index_banner','index_team_background','index_donate_background',
            'index_donate_image','index_video_background']
        )
        images_dict = {image.reference: image for image in images_query}
        staticts_dict = {statics.name: statics for statics in staticts_query}
        videos = VideosWeb.objects.filter(is_short=False).order_by('-publishedAt')[:3]
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
            'video_urls':videos,
            'images':images_dict,
            'data_meta':data_meta,
            'staticts':staticts_dict,
        }
        
        return render(request, self.template_name, context)



class WebProperties(View):
    template_name = 'web/properties/list.html'

    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        data_meta = MetaDataWeb.objects.get(origin='properties')
        base_inscriptions = Inscriptions.objects.filter(status=True).exclude(code_statut__valeur="VE").annotate(
            usa_last=Case(
                When(mun_code__description__icontains="USA", then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        )

        if option == 'proprietes' or option == 'properties':
            all_sale = base_inscriptions.filter(prix_demande__isnull=False)
            all_rent = base_inscriptions.filter(prix_location_demande__isnull=False)
            inscriptions_sale = list(all_sale.filter(usa_last=0).order_by('-prix_demande'))
            inscriptions_rent = list(all_rent.filter(usa_last=0).order_by('-prix_location_demande'))
            inscriptions_usa_sale = list(all_sale.filter(usa_last=1).order_by('-prix_demande'))
            inscriptions_usa_rent = list(all_rent.filter(usa_last=1).order_by('-prix_location_demande'))
            inscriptions = inscriptions_sale + inscriptions_rent + inscriptions_usa_sale + inscriptions_usa_rent

        if option == "properties-for-sale" or option == "proprietes-a-vendre":
            inscriptions = base_inscriptions.filter(prix_demande__isnull=False).order_by('usa_last','-prix_demande')
            data_meta = MetaDataWeb.objects.get(origin='sale')
            
        if option == "properties-for-rent" or option == "proprietes-a-louer":
            inscriptions = base_inscriptions.filter(prix_location_demande__isnull=False).order_by('usa_last','-prix_location_demande')
            data_meta = MetaDataWeb.objects.get(origin='rent')

        paginator = Paginator(inscriptions, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)
        images_query = ImagesWeb.objects.filter(reference__in=['properties_banner'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'data_meta':data_meta,
            'inscriptions':inscriptions,
            'images':images_dict,
        }
        
        return render(request, self.template_name, context)


def searchpropriete(request):
    term = request.GET.get('term')
    status = request.GET.get('status')
    regions = Regions.objects.all()
    municipalites = Municipalites.objects.all()
    inscriptions = Inscriptions.objects.filter(status=True).exclude(code_statut__valeur="VE").annotate(
        usa_last=Case(
            When(mun_code__description__icontains="USA", then=Value(1)),
            default=Value(0),
            output_field=models.IntegerField(),
        )
    ).order_by('usa_last', 'mun_code__description')

    if status == '2':
        inscriptions = inscriptions.filter(prix_location_demande__isnull=False)
    else:
        inscriptions = inscriptions.filter(prix_demande__isnull=False)

    data_dict = {
        "regions": {},
        "municipalites": {},
        "inscriptions": {}
    }

    for region in regions:
        data_dict["regions"][region.id] = {
            "value": region.description_francaise,
            "id": region.code,
            "categorie": "1"
        }

    for mun in municipalites:
        data_dict["municipalites"][mun.id] = {
            "value": mun.description,
            "id": mun.code,
            "categorie": "2",
        }

    for ins in inscriptions:
        data_dict["inscriptions"][ins.id] = {
            "value": "(" + ins.no_inscription +") " + ins.no_civique_debut +" " + ins.nom_rue_complet,
            "id": ins.id,
            "categorie": "4",
        }

    filtered_data = {
        "regions": {k: v for k, v in data_dict["regions"].items() if term.lower() in v["value"].lower()},
        "municipalites": {k: v for k, v in data_dict["municipalites"].items() if term.lower() in v["value"].lower()},
        "inscriptions": {k: v for k, v in data_dict["inscriptions"].items() if term.lower() in v["value"].lower()}
    }

    json_data = {str(i + 1): val for i, val in enumerate(list(filtered_data["regions"].values()) + list(filtered_data["municipalites"].values()) + list(filtered_data["inscriptions"].values()))}
    return JsonResponse(json_data, safe=False)



class SearchView(View):
    template_name = 'web/properties/list.html'
    def get(self, request, *args, **kwargs):

        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        codelang = request.GET.get('Codelang', '')
        status = request.GET.get('status', '')
        adress_region = request.GET.getlist('adress[region][]')
        adress_mun = request.GET.getlist('adress[mun][]')
        nbchambre = request.GET.get('nbchambre', '')
        nbbain = request.GET.get('nbbain', '')
        minamount = request.GET.get('minamount', '')
        maxamount = request.GET.get('maxamount', '')
        propriete = request.GET.getlist('propriete[]')
        query = Q(status=True)
        data_meta = MetaDataWeb.objects.get(origin='properties')

        if propriete:
            proprietes = [item.split('-')[1] for item in propriete]
            try:
                query &= Q(genre_propriete__in=proprietes)
            except Http404:
                print("No se encontraron registros de Inscriptions que cumplan con el filtro.")

        if status == '2':
            query &= Q(prix_location_demande__isnull=False)
        elif status =='1':
            query &= Q(prix_demande__isnull=False)
        else:
            pass

        if nbchambre:
            nbchambre = int(nbchambre)
            query &= Q(nb_chambres__gte=nbchambre)

        if nbbain:
            nbbain = int(nbbain)
            query &= Q(nb_salles_bains__gte=nbbain)

        if minamount:
            minamount = float(minamount)
            if status == '2':
                query &= Q(prix_location_demande__gte=minamount)
            elif status =='1':
                query &= Q(prix_demande__gte=minamount)
            else:
                inscriptions_location = Q(prix_location_demande__gte=minamount)
                inscriptions_demande = Q(prix_demande__gte=minamount)
                query &= (inscriptions_location | inscriptions_demande)

        if maxamount:
            maxamount = float(maxamount)
            if status == '2':
                query &= Q(prix_location_demande__lte=maxamount)
            elif status =='1':
                query &= Q(prix_demande__lte=maxamount)
            else:
                inscriptions_location_max = Q(prix_location_demande__lte=maxamount)
                inscriptions_demande_max = Q(prix_demande__lte=maxamount)
                query &= (inscriptions_location_max | inscriptions_demande_max)

        if adress_mun:
            query &= Q(mun_code__code__in=adress_mun)

        if adress_region:
            query &= Q(mun_code__region_code__in=adress_region)

        inscriptions_all = Inscriptions.objects.exclude(code_statut__valeur="VE").filter(query).annotate(
            usa_last=Case(
                When(mun_code__description__icontains="USA", then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        ).order_by('usa_last', 'mun_code__description')

        paginator = Paginator(inscriptions_all, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)
        images_query = ImagesWeb.objects.filter(reference__in=['properties_banner'])
        images_dict = {image.reference: image for image in images_query}
        
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'codelang': codelang,
            'status': status,
            'nbchambre': nbchambre,
            'nbbain': nbbain,
            'minamount': minamount,
            'maxamount': maxamount,
            'propriete':propriete,
            'inscriptions':inscriptions,
            'data_meta':data_meta,
            'images':images_dict,
        }

        return render(request, self.template_name, context)


class WebDetailProperty(View):

    def get(self, request, *args, **kwargs):
        propertie_id = kwargs.get('propertie_id')
        language = kwargs.get('language', 'fr')

        try: 
            propertie = Inscriptions.objects.get(id=propertie_id, status=True)
            municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
            genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
            labels = DICT_LABELS.get(language).get('web')
            option = kwargs.get('option', 'detail-propertie')
            flag = kwargs.get('flag', 'detail')
            self.template_name = 'web/properties/{}.html'.format(flag)
            mun_code = propertie.mun_code
            same_district = Inscriptions.objects.filter(mun_code=mun_code, status=True).exclude(id=propertie.id)[:4]
            url_pdf = '{}/{}/{}/pdf/'.format(language, option, propertie_id)
            
            taxsco = propertie.depenses.filter(tdep_code__valeur='TAXSCO').first()
            taxmun = propertie.depenses.filter(tdep_code__valeur='TAXMUN').first()
            try:
                total_fees = taxsco.montant_depense + taxmun.montant_depense
            except:
                total_fees = 0
            total_municipal = 0
            addenda_list = Addenda.objects.filter(no_inscription__id=propertie_id)
            addenda_f_list = addenda_list.filter(code_langue__valeur="F")
            addenda_f_texts = []
            for addenda in addenda_f_list:
                if addenda.texte:
                    if addenda.texte.startswith('-'):
                        addenda_f_texts.append('<br>' + addenda.texte)
                    else:
                        if addenda.texte[0].isupper():
                            addenda_f_texts.append('<br><br>')
                            addenda_f_texts.append(addenda.texte)
                        else:
                            addenda_f_texts.append(addenda.texte)
            addenda_f = ' '.join(addenda_f_texts)
            addenda_a_list = addenda_list.filter(code_langue__valeur="A")
            addenda_a_texts = []
            for addenda in addenda_a_list:
                if addenda.texte:
                    if addenda.texte.startswith('-'):
                        addenda_a_texts.append('<br>' + addenda.texte)
                    else:
                        if addenda.texte[0].isupper():
                            addenda_a_texts.append('<br><br>')
                            addenda_a_texts.append(addenda.texte)
                        else:
                            addenda_a_texts.append(addenda.texte)
            addenda_a = ' '.join(addenda_a_texts)
            images_query = ImagesWeb.objects.filter(reference__in=['properties_banner'])
            images_dict = {image.reference: image for image in images_query}

            context = {
                'municipalites':municipalites,
                'genres':genres,
                'language':language,
                'option':option,
                'flag':flag,
                'labels':labels,
                'inscription': propertie,
                'same_district': same_district,
                'total_fees':total_fees,
                'addenda_f':addenda_f,
                'addenda_a':addenda_a,
                'images':images_dict,
                'url_pdf':url_pdf,
            }
            return render(request, self.template_name, context)
            
        except:
            redirect_option = 'properties' if language == 'en' else 'proprietes'
            return redirect("web:properties", language=language, option=redirect_option)
        



class WebPropertyRedirect(View):
    def get(self, request, *args, **kwargs):
        propertie_code = request.GET.get("mls")
        language = kwargs.get('language', 'fr')
        flag = kwargs.get('flag', 'detail')
        option = kwargs.get('option', 'proprietes')
        try: 
            propertie = Inscriptions.objects.get(no_inscription=propertie_code, status=True)
            return redirect( "web:detail-propertie", language=language, option=option, propertie_id=propertie.id, flag=flag)
        except:
            propertie = False
            return redirect("web:properties", language=language, option=option+"s")
            


class WebVideos(View):
    template_name = 'web/videos.html'

    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        videos = VideosWeb.objects.all().order_by('-publishedAt')
        data_meta = MetaDataWeb.objects.get(origin='video')
        images_query = ImagesWeb.objects.filter(reference__in=['videos_banner'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'labels':labels,
            'videos':videos,
            'data_meta':data_meta,
            'images':images_dict,
        }
        return render(request, self.template_name, context)

def search_videos(request):
    print("entro")
    query = request.GET.get("q", "")
    if query:
        videos = VideosWeb.objects.filter(tittle__icontains=query)
        results = [
            {
                "videoId": video.videoId,
                "title": video.tittle,
                "publishedAt": video.publishedAt.strftime("%d/%m/%Y"),
                "description": video.description[:200] + ("..." if len(video.description) > 200 else ""),
                "is_short": video.is_short,
            }
            for video in videos
        ]
    else:
        results = []
    
    print(results)
    return JsonResponse({"videos": results})

class WebContact(View):
    template_name = 'web/contact.html'

    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'contact-courtier-immobilier')
        images_query = ImagesWeb.objects.filter(reference__in=['contact_banner','contact_team_background','contact_team'])
        images_dict = {image.reference: image for image in images_query}
        data_meta = MetaDataWeb.objects.get(origin='contact')

        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'images':images_dict,
            'data_meta':data_meta,
        }

        return render(request, self.template_name, context)

class WebPolicy(View):
    template_name = 'web/policy.html'

    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        images_query = ImagesWeb.objects.filter(reference__in=['privacy_banner'])
        images_dict = {image.reference: image for image in images_query}
        option = kwargs.get('option', 'politique-confidentialite')
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'images':images_dict,
        }
        return render(request, self.template_name, context)

class WebTeam(View):
    template_name = 'web/team.html'
    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        team = Profile.objects.filter(user__is_active=True).exclude(order__isnull=True).order_by('order')
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'courtier-immobilier')
        images_query = ImagesWeb.objects.filter(reference__in=['team_banner'])
        images_dict = {image.reference: image for image in images_query}
        data_meta = MetaDataWeb.objects.get(origin='team')
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'team':team,
            'images':images_dict,
            'data_meta':data_meta,
        }
        return render(request, self.template_name, context)

class WebMemberDetail(View):
    template_name = 'web/member.html'
    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        member_id = kwargs.get('member_id')
        member = get_object_or_404(Profile, membre_id=member_id)
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        images_query = ImagesWeb.objects.filter(reference__in=['team_banner'])
        images_dict = {image.reference: image for image in images_query}
        option = kwargs.get('option', 'courtier-immobilier')
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'member': member,
            'images':images_dict,
            'data_meta':member,
        }
        return render(request, self.template_name, context)


class WebWork(View):
    template_name = 'web/work.html'

    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option')
        type_option = 'one' if option in ['buying','acheter'] else 'two'
        images_query = ImagesWeb.objects.filter(reference__in=['work_banner','work_buy','work_sell','work_next_steps'])
        images_dict = {image.reference: image for image in images_query}
        origin = 'buy' if type_option == 'one' else 'sell'
        data_meta = MetaDataWeb.objects.get(origin=origin)

        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'labels':labels,
            'option':option,
            'type_option':type_option,
            'images':images_dict,
            'data_meta':data_meta,
        }

        return render(request, self.template_name, context)


def calc_monthly_payment_view(request):
    if request.method == 'GET':
        P = float(request.GET.get('hypotheque', 0))
        r_anual = float(request.GET.get('interest_percent', 0))
        n_anos = int(request.GET.get('year_term', 0))

        if P and r_anual and n_anos:
            M = calc_monthly_payment(P, r_anual, n_anos)
            response_data = {'monthly_payment': M}
        else:
            response_data = {'error': 'Invalid parameters'}

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'})


def calc_monthly_payment(P, r_anual, n_anos):
    r_mensual = r_anual / 12 / 100
    n_meses = n_anos * 12
    M = P * (r_mensual * (1 + r_mensual) ** n_meses) / ((1 + r_mensual) ** n_meses - 1)
    return M


def contact_messages(request):
    if request.method == 'POST':
        new = Formulaire_contact()
        new.nom = request.POST.get('prenom')
        new.courriel = request.POST.get('email')
        new.sujet = request.POST.get('sujet')
        new.message = request.POST.get('comment')
        new.adresse = request.POST.get('adresse')
        new.telephone = request.POST.get('tel')
        new.save()
        return JsonResponse({'response': 1})
    else:
        return JsonResponse({'response': 0})

def searchMember(request):
    query = request.GET.get('term')
    language = request.GET.get('Codelang', 'en')
    if query:
        profiles = Profile.objects.filter(
            Q(membre__prenom__icontains=query) |
            Q(membre__nom__icontains=query) |
            Q(membre__bur_code__code__icontains=query)
        ).filter(
            user__is_active=True
        ).exclude(
            order__isnull=True
        ).order_by('order')
    else:
        profiles = Profile.objects.filter(user__is_active=True).exclude(order__isnull=True).order_by('order')

    results = []
    for profile in profiles:
        results.append({
            'name': profile.user.get_full_name(),
            'occupation': profile.occupation if language == 'en' else profile.occupation_anglaise,
            'certification': profile.membre.type_certificat.description_anglaise if language == 'en' else profile.membre.type_certificat.description_francaise,
            'phone': profile.membre.telephone_1,
            'email': profile.membre.courriel,
            'facebook': profile.facebook,
            'instagram': profile.instagram,
            'linkedin': profile.linkedin,
            'twitter': profile.twitter,
            'image': profile.image.url,
            'image_over': profile.image_over.url,
            'id': profile.membre.id,
        })
    return JsonResponse({'results': results})


def statistics(request):
    try:
        sold_price = Statistics.objects.get(name = "sold_price")
    except Statistics.DoesNotExist:
        sold_price = None
    try:
        days = Statistics.objects.get(name="days")
    except Statistics.DoesNotExist:
        days = None
    try:
        number_transactions = Statistics.objects.get(name="number_transactions")
    except Statistics.DoesNotExist:
        number_transactions = None
    if request.method == "POST":
        try:
            sold_price.initial_year = request.POST.get('price_initial_year')
            sold_price.final_year = request.POST.get('price_final_year')
            sold_price.initial_value = request.POST.get('price_initial_value')
            sold_price.final_value = request.POST.get('price_final_value')
            sold_price.save()
        except:
            pass
        try:
            days.initial_year = request.POST.get('day_initial_year')
            days.final_year = request.POST.get('day_final_year')
            days.initial_value = request.POST.get('day_initial_value')
            days.final_value = request.POST.get('day_final_value')
            days.save()
        except:
            pass
        try:
            number_transactions.initial_year = request.POST.get('number_initial_year')
            number_transactions.final_year = request.POST.get('number_final_year')
            number_transactions.initial_value = request.POST.get('number_initial_value')
            number_transactions.final_value = request.POST.get('number_final_value')
            number_transactions.save()
        except:
            pass
        messages.success(request, 'Datos actualizados correctamente!')
        return redirect("web:statistics")

    context = {
        'sold_price':sold_price,
        'days':days,
        'number_transactions':number_transactions,
    }
    return render(request, 'statistics.html', context)

class SearchProperties(ListView):
    template_name = 'web/properties/list.html'
    
    def get(self, request, *args, **kwargs):
        municipalites = Municipalites.objects.filter(municipalite_code__isnull=False).distinct()
        genres = GenresProprietes.objects.filter(genre_proprietes__isnull=False).distinct()
        language = self.kwargs.get('language', 'fr')
        option = self.kwargs.get('option', 'proprietes')
        parts = option.split('-')
        filter = parts[-1]
        code = parts[-2]
        if filter== "quartier":
            inscriptions_all = Inscriptions.objects.filter(mun_code=code)
        if filter== "categorie":
            code = code.upper()
            inscriptions_all = Inscriptions.objects.filter(genre_propriete=code)

        labels = DICT_LABELS.get(language).get('web')
        
        paginator = Paginator(inscriptions_all, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)
        images_query = ImagesWeb.objects.filter(reference__in=['properties_banner'])
        images_dict = {image.reference: image for image in images_query}
        data_meta = MetaDataWeb.objects.get(origin='properties')
        
        context = {
            'municipalites':municipalites,
            'genres':genres,
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
            'images':images_dict,
            'data_meta':data_meta,
        }

        return render(request, self.template_name, context)




def metadata(request):
    objects = MetaDataWeb.objects.all()
    return render(request, 'web/metadata/list.html',{'objects':objects})


def update_metadata(request, pk):
    meta = get_object_or_404(MetaDataWeb, id=pk)
    if request.method == 'POST':
        meta_form = MetadataForm(request.POST, instance=meta)
        if meta_form.is_valid():
            meta_form.save()
            messages.success(request, 'Metadata actualizada', 'succesful')
            return redirect('web:list-metadata')  
        else:
            messages.error(request, 'Error al actualizar la Metadata')
    else:
        meta_form = MetadataForm(instance=meta)
    
    return render(request, 'web/metadata/update.html', {'meta_form': meta_form})

