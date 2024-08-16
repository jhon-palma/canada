import pdb
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.contrib import auth,messages
from django.core.paginator import Paginator
# from django.db.models import F, Q
from django.db.models import Value, CharField, Q
from django.template.loader import *
from django.urls import reverse
from django.views.decorators.csrf import *
from django.views.generic import *
from django.shortcuts import get_object_or_404
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from dateutil.relativedelta import *
from datetime import *
from apps.users.models import Profile
from apps.web.models import Formulaire_contact, ImagesWeb, Statistics, VideosWeb
from immobilier.local_settings import CHANNEL_ID, KEY_API_YB
from ..properties.models import Addenda, Caracteristiques, GenresProprietes, Inscriptions, Membres, Municipalites, Propertie, Regions, SousTypeCaracteristiques
from ..labels import DICT_LABELS
# import os, time, json, httplib2, requests
import requests
from googleapiclient.discovery import build
import isodate
from django.utils.dateparse import parse_datetime



def get_youtube_videos(api_key, channel_id, max_results):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Obtener lista de videos del canal
    videos_request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=30,
        order='date',
        type='video',
    )
    videos_response = videos_request.execute()
    videos = []

    for item in videos_response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        publishedAt = item['snippet']['publishedAt']
        description = item['snippet']['description']

        video_details_request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        video_details_response = video_details_request.execute()

        duration = video_details_response['items'][0]['contentDetails']['duration']

        duration_seconds = isodate.parse_duration(duration).total_seconds()
        published_datetime = datetime.fromisoformat(publishedAt.replace('Z', '+00:00'))
        if duration_seconds > 91:
            videos.append({
                'title': video_title,
                'video_id': video_id,
                'publishedAt': published_datetime,
                'description': description,
            })
        if len(videos) >= max_results:
            break

    return videos


class WebIndex(View):
    template_name = 'web/index.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        inscriptions = Inscriptions.objects.all().order_by('-id')[:3]
        inscriptions_vendu = Inscriptions.objects.select_related('code_statut').filter(code_statut__valeur="VE")
        staticts_query = Statistics.objects.all()
        images_query = ImagesWeb.objects.filter(reference__in=[
            'index_banner','index_team_background','index_donate_background',
            'index_donate_image','index_video_background']
        )
        images_dict = {image.reference: image for image in images_query}
        staticts_dict = {statics.name: statics for statics in staticts_query}
        videos = VideosWeb.objects.filter(is_short=False).order_by('-publishedAt')[:3]
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
            'inscriptions_vendu':inscriptions_vendu,
            'video_urls':videos,
            'images':images_dict,
            'staticts':staticts_dict,
        }
        return render(request, self.template_name, context)



class WebProperties(View):
    template_name = 'web/properties/list.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        if option == "properties-for-sale" or option == "proprietes-a-vendre":
            inscriptions_all = Inscriptions.objects.filter(prix_demande__isnull=False)
        elif option == "properties-for-rent" or option == "proprietes-a-louer":
            inscriptions_all = Inscriptions.objects.filter(prix_location_demande__isnull=False)
        else:
            inscriptions_all = Inscriptions.objects.all()
        paginator = Paginator(inscriptions_all, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)
        images_query = ImagesWeb.objects.filter(reference__in=['properties_banner'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



def searchpropriete(request):
    term = request.GET.get('term')
    status = request.GET.get('status')
    regions = Regions.objects.all()
    municipalites = Municipalites.objects.all()
    if status == '2':
        inscriptions = Inscriptions.objects.filter(prix_location_demande__isnull=False)
        inscriptions = Inscriptions.objects.filter(prix_demande__isnull=False)

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
        query = Q()

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

        inscriptions_all = Inscriptions.objects.filter(query)
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
            'images':images_dict,
        }

        return render(request, self.template_name, context)



class WebDetailProperty(View):
    template_name = 'web/properties/detail.html'
    def get(self, request, *args, **kwargs):
        propertie_id = kwargs.get('propertie_id')
        propertie = get_object_or_404(Inscriptions, id=propertie_id)
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'detail-propertie')
        mun_code = propertie.mun_code
        same_district = Inscriptions.objects.filter(mun_code=mun_code).exclude(id=propertie.id)[:4]

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
            'language':language,
            'option':option,
            'labels':labels,
            'inscription': propertie,
            'same_district': same_district,
            'total_fees':total_fees,
            'addenda_f':addenda_f,
            'addenda_a':addenda_a,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebVideos(View):
    template_name = 'web/videos.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        videos = VideosWeb.objects.filter(is_short=False).order_by('-publishedAt')
        images_query = ImagesWeb.objects.filter(reference__in=['videos_banner'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'language':language,
            'labels':labels,
            'videos':videos,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebContact(View):
    template_name = 'web/contact.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'contact-courtier-immobilier')
        images_query = ImagesWeb.objects.filter(reference__in=['contact_banner','contact_team_background','contact_team'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebPolicy(View):
    template_name = 'web/policy.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        images_query = ImagesWeb.objects.filter(reference__in=['privacy_banner'])
        images_dict = {image.reference: image for image in images_query}
        option = kwargs.get('option', 'politique-confidentialite')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebTeam(View):
    template_name = 'web/team.html'
    def get(self, request, *args, **kwargs):
        team = Profile.objects.filter(user__is_active=True).exclude(order__isnull=True).order_by('order')
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'courtier-immobilier')
        images_query = ImagesWeb.objects.filter(reference__in=['team_banner'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'team':team,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebMemberDetail(View):
    template_name = 'web/member.html'
    def get(self, request, *args, **kwargs):
        member_id = kwargs.get('member_id')
        member = get_object_or_404(Profile, membre_id=member_id)
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        images_query = ImagesWeb.objects.filter(reference__in=['team_banner'])
        images_dict = {image.reference: image for image in images_query}
        option = kwargs.get('option', 'courtier-immobilier')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'member': member,
            'images':images_dict,
        }
        return render(request, self.template_name, context)



class WebWork(View):
    template_name = 'web/work.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'travailler-avec-nous')
        images_query = ImagesWeb.objects.filter(reference__in=['work_banner','work_buy','work_sell','work_next_steps'])
        images_dict = {image.reference: image for image in images_query}
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'images':images_dict,
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