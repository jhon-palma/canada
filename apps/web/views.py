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
from django.views.decorators.csrf import *
from django.views.generic import *
from django.shortcuts import get_object_or_404
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from dateutil.relativedelta import *
from datetime import *
from apps.users.models import Profile
from apps.web.models import Formulaire_contact
from ..properties.models import Addenda, Caracteristiques, Inscriptions, Membres, Municipalites, Propertie, Regions, SousTypeCaracteristiques
from ..labels import DICT_LABELS
# import os, time, json, httplib2, requests



class WebIndex(View):
    template_name = 'web/index.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        inscriptions = Inscriptions.objects.all().order_by('-id')[:3]
        # inscriptions_vendu = Inscriptions.objects.all()
        inscriptions_vendu = Inscriptions.objects.select_related('code_statut').filter(code_statut__valeur="VE")
        # print(inscriptions_vendu)
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
            'inscriptions_vendu':inscriptions_vendu,
        }
        return render(request, self.template_name, context)

class WebProperties(View):
    template_name = 'web/properties/list.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        option = kwargs.get('option', 'proprietes')
        labels = DICT_LABELS.get(language).get('web')
        inscriptions_all = Inscriptions.objects.all()
        paginator = Paginator(inscriptions_all, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'inscriptions':inscriptions,
        }
        return render(request, self.template_name, context)

def searchpropriete(request):
    term = request.GET.get('term')
    status = request.GET.get('status')
    regions = Regions.objects.all()
    municipalites = Municipalites.objects.all()
    # inscriptions = Inscriptions.objects.all()
    if status == '2':
        inscriptions = Inscriptions.objects.filter(prix_location_demande__isnull=False)
    else:
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
    # print(json_data)
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
        
        # print("codelang: ",codelang)
        # print("status: ",status)
        # print('adress_region: ',adress_region)
        # print('adress_mun: ',adress_mun)
        # print("nbchambre: ",nbchambre)
        # print("nbbain: ",nbbain)
        # print("minamount: ",minamount)
        # print("maxamount: ",maxamount)
        # print('propriete: ', propriete)
        query = Q()
        
        if status == '2':
            query &= Q(prix_location_demande__isnull=False)
        elif status =='1':
            query &= Q(prix_demande__isnull=False)
        else:
            pass
            # query &= Q(prix_location_demande__isnull=False) & Q(prix_demande__isnull=False)

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
                # inscriptions_location = Inscriptions.objects.filter(prix_location_demande__gte=minamount)
                # inscriptions_demande = Inscriptions.objects.filter(prix_demande__gte=minamount)
                # inscriptions_prix = inscriptions_location.union(inscriptions_demande)
                inscriptions_location = Q(prix_location_demande__gte=minamount)
                inscriptions_demande = Q(prix_demande__gte=minamount)
                query &= (inscriptions_location | inscriptions_demande)

        if maxamount:
            print(maxamount)
            maxamount = float(maxamount)
            if status == '2':
                query &= Q(prix_location_demande__lte=maxamount)
            elif status =='1':
                query &= Q(prix_demande__lte=maxamount)
            else:
                # inscriptions_location = Inscriptions.objects.filter(prix_location_demande__lte=maxamount)
                # inscriptions_demande = Inscriptions.objects.filter(prix_demande__lte=maxamount)
                # inscriptions_prix = inscriptions_location.union(inscriptions_demande)
                inscriptions_location_max = Q(prix_location_demande__lte=maxamount)
                inscriptions_demande_max = Q(prix_demande__lte=maxamount)
                query &= (inscriptions_location_max | inscriptions_demande_max)

        # inscriptions_mun = Inscriptions.objects.none()
        # inscriptions_region = Inscriptions.objects.none()

        if adress_mun:
            # inscriptions_mun = Inscriptions.objects.filter(query & Q(mun_code__code__in=adress_mun))
            query &= Q(mun_code__code__in=adress_mun)

        if adress_region:
            # inscriptions_region = Inscriptions.objects.filter(query & Q(mun_code__region_code__in=adress_region))
            query &= Q(mun_code__region_code__in=adress_region)

        # inscriptions_combined = set(inscriptions_mun) | set(inscriptions_region)
        
        # inscriptions = list(inscriptions_combined)

        inscriptions_all = Inscriptions.objects.filter(query)

        num_results = len(inscriptions_all)
        print("===================: ",query)
        if num_results == 0:
            inscriptions_all = Inscriptions.objects.filter(query)
            print('LEN: ',len(inscriptions_all))
        # for i in inscriptions:
        #     print(i.no_inscription)
        print('num_results: ',num_results)

        paginator = Paginator(inscriptions_all, 36)
        page_number = request.GET.get('page')
        inscriptions = paginator.get_page(page_number)

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
            'inscriptions':inscriptions,
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
        # caracteristicas_filtradas = Caracteristiques.objects.filter(no_inscription=propertie_id)
        # caracteristicas_con_descripcion = []
        # for caracteristica in caracteristicas_filtradas:
        #     sous_type = SousTypeCaracteristiques.objects.get(
        #         tcar_code=caracteristica.tcar_code,
        #         code=caracteristica.scarac_code.code
        #     )
        #     caracteristica.description_francaise = sous_type.description_francaise
        #     caracteristica.description_anglaise = sous_type.description_anglaise
        #     caracteristica.tcar_code_value = sous_type.tcar_code.code
        #     caracteristica.scarac_code_value = sous_type.code
        #     caracteristicas_con_descripcion.append(caracteristica)
        
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
        # addenda_f = ' '.join([addenda.texte for addenda in addenda_f_list if addenda.texte])
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
        # addenda_a = ' '.join([addenda.texte for addenda in addenda_a_list if addenda.texte])
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'inscription': propertie,
            'same_district': same_district,
            'total_fees':total_fees,
            'addenda_f':addenda_f,
            'addenda_a':addenda_a,
        }
        return render(request, self.template_name, context)

class WebVideos(View):
    template_name = 'web/videos.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        context = {
            'language':language,
            'labels':labels,
        }
        return render(request, self.template_name, context)

class WebContact(View):
    template_name = 'web/contact.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'contact-courtier-immobilier')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
        }
        return render(request, self.template_name, context)
    
class WebPolicy(View):
    template_name = 'web/policy.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'politique-confidentialite')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
        }
        return render(request, self.template_name, context)

class WebTeam(View):
    template_name = 'web/team.html'
    def get(self, request, *args, **kwargs):
        team = Profile.objects.filter(user__is_active=True).exclude(order__isnull=True).order_by('order')
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'courtier-immobilier')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'team': team,
        }
        return render(request, self.template_name, context)

class WebMemberDetail(View):
    template_name = 'web/member.html'
    def get(self, request, *args, **kwargs):
        member_id = kwargs.get('member_id')
        member = get_object_or_404(Profile, membre_id=member_id)
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'courtier-immobilier')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
            'member': member,
        }
        return render(request, self.template_name, context)

class WebWork(View):
    template_name = 'web/work.html'

    def get(self, request, *args, **kwargs):
        language = kwargs.get('language', 'fr')
        labels = DICT_LABELS.get(language).get('web')
        option = kwargs.get('option', 'travailler-avec-nous')
        context = {
            'language':language,
            'option':option,
            'labels':labels,
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
