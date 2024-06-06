from django.apps import apps
from django.db.models import ForeignKey
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone
import pdb
import csv

from .models import *
# UPLOAD DATA TO POPULATE THE GENERIC TABLES OF THE DATABASE
# UPLOAD GENERIC DATA
# IMPORTANT! To do it in this order
#       VALEURS_FIXES
#       REGIONS
#       MUNICIPALITES
#       QUARTIERS
#       TYPES_BANNIERES
#       GENRES_PROPRIETES
#       TYPE_CARACTERISTIQUES
#       SOUS_TYPE_CARACTERISTIQUES
# UPLOAD DOWNLOADED DATA
# IMPORTANT! To do it in this order
    #   FIRMES
    #   BUREAUX
    #   MEMBRES
    #   MEMBRES_MEDIAS_SOCIAUX
    #   INSCRIPTIONS
    #   PHOTOS
    #   LIENS_ADDITIONNELS
    #   VISITES_LIBRES
    #   REMARQUES
    #   UNITES_DETAILLEES
    #   ADDENDA
    #   UNITES_SOMMAIRES
    #   DEPENSES
    #   RENOVATIONS
    #   PIECES_UNITES
    #   CARACTERISTIQUES


def process_txt_data(file_path):
    data = []
    with open(file_path, encoding='latin-1') as txt_file:
        for line in txt_file:
            line = line.strip()
            reader = csv.reader([line])
            fields = next(reader)
            data.append(fields)
    return data


def get_model_by_meta_name(model_name):
    for model in apps.get_models():
        if hasattr(model._meta, 'db_table') and model._meta.db_table == model_name:
            return model
    return None

def get_model_fields(model):
    fields = []
    for field in model._meta.fields:
        if field.name != 'id':
            fields.append(field.name)
    return fields

def create_objects(data, model_name):
    mensaje = ""

    model = get_model_by_meta_name(model_name)
    # if model_name == "QUARTIERS":
    if model_name == "FIRMES":
        mensaje = uploadFirmes(data)
    elif model_name == "BUREAUX":
        mensaje = uploadBureaux(data)
    elif model_name == "MEMBRES":
        mensaje = uploadMembres(data)
    elif model_name == "MEMBRES_MEDIAS_SOCIAUX":
        mensaje = uploadMembresMediasSociaux(data)
    elif model_name == "INSCRIPTIONS":
        mensaje = uploadInscriptions(data)
        return mensaje
    elif model_name == "PHOTOS":
        mensaje = uploadPhotos(data)
        return mensaje
    elif model_name == "LIENS_ADDITIONNELS":
        mensaje = uploadLiensAdditionnels(data)
        return mensaje
    elif model_name == "VISITES_LIBRES":
        mensaje = uploadVisitesLibres(data)
        return mensaje
    elif model_name == "REMARQUES":
        mensaje = uploadRemarques(data)
        return mensaje
    elif model_name == "UNITES_DETAILLEES":
        mensaje = uploadUnitesDetaillees(data)
        return mensaje
    elif model_name == "ADDENDA":
        mensaje = uploadAddenda(data)
        return mensaje
    elif model_name == "UNITES_SOMMAIRES":
        mensaje = uploadUnitesSommaires(data)
        return mensaje
    elif model_name == "DEPENSES":
        mensaje = uploadDepenses(data)
        return mensaje
    elif model_name == "RENOVATIONS":
        mensaje = uploadRenovations(data)
        return mensaje
    elif model_name == "PIECES_UNITES":
        mensaje = uploadPiecesUnites(data)
        return mensaje
    elif model_name == "CARACTERISTIQUES":
        mensaje = uploadCaracteristiques(data)
        return mensaje
    else:
        mensaje = uploadDataGeneric(data, model_name)

    return mensaje

def uploadDataGeneric(data, model_name):
    model = get_model_by_meta_name(model_name)
    fields = get_model_fields(model)
    repetidos = 0
    total_nuevos = 0
    if fields:
        foreign_keys = []
        for field in fields:
            campo = model._meta.get_field(field)
            if isinstance(campo, ForeignKey):
                foreign_keys.append(campo.name)
    for row in data:
        if model_name == "VALEURS_FIXES":
            domaine_value = row[0]
            valeur_value = row[1]
            if model.objects.filter(domaine=domaine_value, valeur=valeur_value).exists():
                repetidos = repetidos + 1
                continue
        elif model_name == "QUARTIERS":
            mun_code = row[0]
            code = row[1]
            if model.objects.filter(mun_code=mun_code, code=code).exists():
                repetidos = repetidos + 1
                continue
        elif model_name == "GENRES_PROPRIETES":
            categorie_propriete = row[0]
            genre_propriete = row[1]
            if model.objects.filter(categorie_propriete=categorie_propriete, genre_propriete=genre_propriete).exists():
                repetidos = repetidos + 1
                continue
        elif model_name == "SOUS_TYPE_CARACTERISTIQUES":
            tcar_code = row[0]
            code = row[1]
            if model.objects.filter(tcar_code=tcar_code, code=code).exists():
                repetidos = repetidos + 1
                continue
        elif model_name == "MEMBRES_MEDIAS_SOCIAUX":
            membre_code = row[0]
            valor_valeurs_fixes = row[1]
            type_media_social = get_id_valeurs(valor_valeurs_fixes,'TYPE_MEDIA_SOCIAL')
            if model.objects.filter(membre_code=membre_code, type_media_social=type_media_social).exists():
                repetidos = repetidos + 1
                continue
        else:
            code = row[0]
            if model.objects.filter(code=code).exists():
                repetidos = repetidos + 1
                continue

        model_instance = model()
        for field_name, value in zip(fields, row):
            if field_name in foreign_keys:
                modelo_relacionado = model._meta.get_field(field_name).related_model
                foreign_key_field = model._meta.get_field(field_name)
                campo = model._meta.get_field(field_name)
                if hasattr(campo, 'related_model') and hasattr(campo.remote_field, 'related_name'):
                    if(modelo_relacionado.__name__ == "ValeursFixes"):
                        relacion_inversa = campo.related_model._meta.get_field(campo.remote_field.related_name)
                        if value:
                            related_object = modelo_relacionado.objects.get(**{'domaine': relacion_inversa.name,'valeur':value})
                        else:
                            related_object = None
                    else:
                        to_field_value = foreign_key_field.to_fields[0] if hasattr(foreign_key_field, 'to_fields') else None
                        related_object = modelo_relacionado.objects.get(**{to_field_value: value})
                else:
                    to_field_value = foreign_key_field.to_fields[0] if hasattr(foreign_key_field, 'to_fields') else None
                    related_object = modelo_relacionado.objects.get(**{to_field_value: value})

                value = related_object if related_object else None
            setattr(model_instance, field_name, value)
        model_instance.save()
        total_nuevos = total_nuevos + 1
    mensaje = f"{total_nuevos} Registros subidos exitosamente en el modelo {model_name}, y se encontraron {repetidos} registros repetidos"
    return mensaje

def uploadFirmes(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0

    for row in data:
        code = row[0]
        nom_legal = row[1] if row[1] else None
        no_certificat = row[2] if row[2] else None
        valor_valeurs_fixes = row[3]
        type_certificat = get_id_valeurs(valor_valeurs_fixes,'TYPE_CERTIFICAT_FIRME')
        banniere_code = TypesBannieres.objects.get(code=row[4])
        firme_principale = row[5] if row[5] else None
        courtier_code = row[6] if row[6] else None
        try:
            firme = Firmes.objects.get(code=code)
            cambios = []
            if firme.nom_legal != nom_legal:
                firme.nom_legal = nom_legal
                cambios.append('nom_legal')
            if firme.no_certificat != no_certificat:
                firme.no_certificat = no_certificat
                cambios.append('no_certificat')
            if firme.type_certificat != type_certificat:
                firme.type_certificat = type_certificat
                cambios.append('type_certificat')
            if firme.banniere_code != banniere_code:
                firme.banniere_code = banniere_code
                cambios.append('banniere_code')
            if firme.firme_principale != firme_principale:
                firme.firme_principale = firme_principale
                cambios.append('firme_principale')
            if firme.courtier_code != courtier_code:
                firme.courtier_code = courtier_code
                cambios.append('courtier_code')

            if cambios:
                firme.save()
                total_actualizadas = total_actualizadas + 1

        except ObjectDoesNotExist:

            firme = Firmes.objects.create(
                code = code,
                nom_legal = nom_legal,
                no_certificat = no_certificat,
                type_certificat = type_certificat,
                banniere_code = banniere_code,
                firme_principale = firme_principale,
                courtier_code = courtier_code,
            )
            total_nuevas = total_nuevas + 1

        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {nom_legal}, revise la base de datos"

    mensaje = f"Firmes creadas: {total_nuevas}, Firmes Actualizadas: {total_actualizadas}"
    return mensaje

def uploadBureaux(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0

    for row in data:
        code = row[0]
        firme_code = Firmes.objects.get(code=row[1])
        nom_legal = row[2] if row[2] else None
        no_civique = row[3] if row[3] else None
        nom_rue = row[4] if row[4] else None
        bureau = row[5] if row[5] else None
        municipalite = row[6] if row[6] else None
        province = row[7] if row[7] else None
        code_postal = row[8] if row[8] else None
        telephone_1 = row[9] if row[9] else None
        poste_1 = row[10] if row[10] else None
        telephone_2 = row[11] if row[11] else None
        poste_2 = row[2] if row[2] else None
        telephone_fax = row[12] if row[12] else None
        courriel = row[13] if row[13] else None
        site_web = row[14] if row[14] else None
        directeur_code = row[15] if row[15] else None
        url_logo_bureau = row[16] if row[16] else None
        try:
            bureaux = Bureaux.objects.get(code=code)
            cambios = []

            if bureaux.firme_code != firme_code:
                bureaux.firme_code = firme_code
                cambios.append('firme_code')
            if bureaux.nom_legal != nom_legal:
                bureaux.nom_legal = nom_legal
                cambios.append('nom_legal')
            if bureaux.no_civique != no_civique:
                bureaux.no_civique = no_civique
                cambios.append('no_civique')
            if bureaux.nom_rue != nom_rue:
                bureaux.nom_rue = nom_rue
                cambios.append('nom_rue')
            if bureaux.bureau != bureau:
                bureaux.bureau = bureau
                cambios.append('bureau')
            if bureaux.municipalite != municipalite:
                bureaux.municipalite = municipalite
                cambios.append('municipalite')
            if bureaux.province != province:
                bureaux.province = province
                cambios.append('province')
            if bureaux.code_postal != code_postal:
                bureaux.code_postal = code_postal
                cambios.append('code_postal')
            if bureaux.telephone_1 != telephone_1:
                bureaux.telephone_1 = telephone_1
                cambios.append('telephone_1')
            if bureaux.poste_1 != poste_1:
                bureaux.poste_1 = poste_1
                cambios.append('poste_1')
            if bureaux.telephone_2 != telephone_2:
                bureaux.telephone_2 = telephone_2
                cambios.append('telephone_2')
            if bureaux.poste_2 != poste_2:
                bureaux.poste_2 = poste_2
                cambios.append('poste_2')
            if bureaux.telephone_fax != telephone_fax:
                bureaux.telephone_fax = telephone_fax
                cambios.append('telephone_fax')
            if bureaux.courriel != courriel:
                bureaux.courriel = courriel
                cambios.append('courriel')
            if bureaux.site_web != site_web:
                bureaux.site_web = site_web
                cambios.append('site_web')
            if bureaux.directeur_code != directeur_code:
                bureaux.directeur_code = directeur_code
                cambios.append('directeur_code')
            if bureaux.url_logo_bureau != url_logo_bureau:
                bureaux.url_logo_bureau = url_logo_bureau
                cambios.append('url_logo_bureau')

            if cambios:
                bureaux.save()
                total_actualizadas = total_actualizadas + 1

        except ObjectDoesNotExist:
            bureaux = Bureaux.objects.create(
                code = code,
                firme_code = firme_code,
                nom_legal = nom_legal,
                no_civique = no_civique,
                nom_rue = nom_rue,
                bureau = bureau,
                municipalite = municipalite,
                province = province,
                code_postal = code_postal,
                telephone_1 = telephone_1,
                poste_1 = poste_1,
                telephone_2 = telephone_2,
                poste_2 = poste_2,
                telephone_fax = telephone_fax,
                courriel = courriel,
                site_web = site_web,
                directeur_code = directeur_code,
                url_logo_bureau = url_logo_bureau,
            )
            total_nuevas = total_nuevas + 1

        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {nom_legal}, revise la base de datos"

    mensaje = f"Bureaux creadas: {total_nuevas}, Bureaux Actualizadas: {total_actualizadas}"
    return mensaje

def uploadMembres(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0

    for row in data:
        code = row[0] if row[0] else None
        b_code = row[1]
        bur_code = get_id_bureau(b_code)
        no_certificat = row[2] if row[2] else None
        valor_valeurs_fixes = row[3]
        type_certificat = get_id_valeurs(valor_valeurs_fixes,'TYPE_CERTIFICAT_MEMBRE')
        nom = row[4] if row[4] else None
        prenom = row[5] if row[5] else None
        titre_professionnel = row[6] if row[6] else None
        champ_inutilise_1 = row[7] if row[7] else None
        telephone_1 = row[8] if row[8] else None
        telephone_2 = row[9] if row[9] else None
        telephone_fax = row[10] if row[10] else None
        courriel = row[11] if row[11] else None
        site_web = row[12] if row[12] else None
        champ_inutilise_2 = row[13] if row[13] else None
        valor_valeurs_fixes = row[14]
        code_langue = get_id_valeurs(valor_valeurs_fixes,'CODE_LANGUE')
        photo_url = row[15] if row[15] else None
        date_modification = row[16] if row[16] else None
        nom_societe = row[17] if row[17] else None
        type_societe_desc_f = row[18] if row[18] else None
        type_societe_desc_a = row[19] if row[19] else None
        lien_video_f = row[20] if row[20] else None
        lien_video_a = row[21] if row[21] else None
        presentation_f = row[22] if row[22] else None
        presentation_a = row[23] if row[23] else None
        try:
            membres = Membres.objects.get(code=code)
            cambios = []

            if membres.bur_code != bur_code:
                membres.bur_code = bur_code
                cambios.append('bur_code')
            if membres.no_certificat != no_certificat:
                membres.no_certificat = no_certificat
                cambios.append('no_certificat')
            if membres.type_certificat != type_certificat:
                membres.type_certificat = type_certificat
                cambios.append('type_certificat')
            if membres.nom != nom:
                membres.nom = nom
                cambios.append('nom')
            if membres.prenom != prenom:
                membres.prenom = prenom
                cambios.append('prenom')
            if membres.titre_professionnel != titre_professionnel:
                membres.titre_professionnel = titre_professionnel
                cambios.append('titre_professionnel')
            if membres.champ_inutilise_1 != champ_inutilise_1:
                membres.champ_inutilise_1 = champ_inutilise_1
                cambios.append('champ_inutilise_1')
            if membres.telephone_1 != telephone_1:
                membres.telephone_1 = telephone_1
                cambios.append('telephone_1')
            if membres.telephone_2 != telephone_2:
                membres.telephone_2 = telephone_2
                cambios.append('telephone_2')
            if membres.telephone_fax != telephone_fax:
                membres.telephone_fax = telephone_fax
                cambios.append('telephone_fax')
            if membres.courriel != courriel:
                membres.courriel = courriel
                cambios.append('courriel')
            if membres.site_web != site_web:
                membres.site_web = site_web
                cambios.append('site_web')
            if membres.champ_inutilise_2 != champ_inutilise_2:
                membres.champ_inutilise_2 = champ_inutilise_2
                cambios.append('champ_inutilise_2')
            if membres.code_langue != code_langue:
                membres.code_langue = code_langue
                cambios.append('code_langue')
            if membres.photo_url != photo_url:
                membres.photo_url = photo_url
                cambios.append('photo_url')
            if membres.date_modification != date_modification:
                membres.date_modification = date_modification
                cambios.append('date_modification')
            if membres.nom_societe != nom_societe:
                membres.nom_societe = nom_societe
                cambios.append('nom_societe')
            if membres.type_societe_desc_f != type_societe_desc_f:
                membres.type_societe_desc_f = type_societe_desc_f
                cambios.append('type_societe_desc_f')
            if membres.type_societe_desc_a != type_societe_desc_a:
                membres.type_societe_desc_a = type_societe_desc_a
                cambios.append('type_societe_desc_a')
            if membres.lien_video_f != lien_video_f:
                membres.lien_video_f = lien_video_f
                cambios.append('lien_video_f')
            if membres.lien_video_a != lien_video_a:
                membres.lien_video_a = lien_video_a
                cambios.append('lien_video_a')
            if membres.presentation_f != presentation_f:
                membres.presentation_f = presentation_f
                cambios.append('presentation_f')
            if membres.presentation_a != presentation_a:
                membres.presentation_a = presentation_a
                cambios.append('presentation_a')

            if cambios:
                membres.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            membres = Membres.objects.create(
                code = code,
                bur_code = bur_code,
                no_certificat = no_certificat,
                type_certificat = type_certificat,
                nom = nom,
                prenom = prenom,
                titre_professionnel = titre_professionnel,
                champ_inutilise_1 = champ_inutilise_1,
                telephone_1 = telephone_1,
                telephone_2 = telephone_2,
                telephone_fax = telephone_fax,
                courriel = courriel,
                site_web = site_web,
                champ_inutilise_2 = champ_inutilise_2,
                code_langue = code_langue,
                photo_url = photo_url,
                date_modification = date_modification,
                nom_societe = nom_societe,
                type_societe_desc_f = type_societe_desc_f,
                type_societe_desc_a = type_societe_desc_a,
                lien_video_f = lien_video_f,
                lien_video_a = lien_video_a,
                presentation_f = presentation_f,
                presentation_a = presentation_a,
            )
            total_nuevas = total_nuevas + 1

        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {code}, revise la base de datos"

    mensaje = f"Membres creadas: {total_nuevas}, Membres Actualizadas: {total_actualizadas}"
    return mensaje

def uploadMembresMediasSociaux(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0

    for row in data:
        membre_code = Membres.objects.get(code=row[0])
        valor_valeurs_fixes = row[1]
        type_media_social = get_id_valeurs(valor_valeurs_fixes,'TYPE_MEDIA_SOCIAL')
        lien_media_social = row[2] if row[2] else None
        try:
            membresMedia = MembresMediasSociaux.objects.get(membre_code=membre_code, type_media_social=type_media_social)
            cambios = []
            # pdb.set_trace()
            if membresMedia.lien_media_social != lien_media_social:
                membresMedia.lien_media_social = lien_media_social
                cambios.append('lien_media_social')
            if cambios:
                membresMedia.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            membresMedia = MembresMediasSociaux.objects.create(
                membre_code = membre_code,
                type_media_social = type_media_social,
                lien_media_social = lien_media_social,
            )
            total_nuevas = total_nuevas + 1

        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {membre_code}, revise la base de datos"

    mensaje = f"MembresMediasSociaux creadas: {total_nuevas}, MembresMediasSociaux Actualizadas: {total_actualizadas}"
    return mensaje

def uploadInscriptions(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0

    new_inscription_keys = {(row[0]) for row in data}

    existing_inscription_keys = {(inscription.no_inscription) for inscription in Inscriptions.objects.all()}

    for existing_key in existing_inscription_keys - new_inscription_keys:
        try:
            inscription_to_delete = Inscriptions.objects.get(
                no_inscription=existing_key,
            )
            inscription_to_delete.delete()
            mensaje += f"Inscrptions eliminada: {existing_key}\n"
        except Inscriptions.DoesNotExist:
            mensaje += f"Error: No se encontró la Inscriptions a eliminar: {existing_key}\n"

    for row in data:
        no_inscription = row[0]
        champ_inutilise_1 = row[1] if row[1] else None
        courtier_inscripteur_1 = get_id_courtier(row[2])
        bureau_inscripteur_1 = get_id_bureau(row[3])
        courtier_inscripteur_2 = get_id_courtier(row[4])
        bureau_inscripteur_2 = get_id_bureau(row[5])
        prix_demande = float(row[6]) if row[6] else None
        devise_prix_demande = row[8] if row[8] else None
        prix_location_demande = float(row[9]) if row[9] else None
        valor_valeurs_fixes = row[7]
        um_prix_demande = get_id_valeurs(valor_valeurs_fixes,'UM_PRIX')
        valor_valeurs_fixes = row[10]
        um_prix_location_demande = get_id_valeurs(valor_valeurs_fixes,'UM_PRIX')
        devise_prix_location_demande = row[11] if row[11] else None
        champ_inutilise_36 = row[12] if row[12] else None
        code_declaration_vendeur = get_id_valeurs(row[13],'CODE_DECLARATION_VENDEUR')
        ind_reprise_finance = get_id_valeurs(row[13],'IND_REPRISE_FINANCE')
        ind_internet = row[15] if row[15] else None
        ind_echange_possible = row[16] if row[16] else None
        champ_inutilise_37 = row[17] if row[17] else None
        champ_inutilise_3 = row[18] if row[18] else None
        champ_inutilise_4 = row[19] if row[19] else None
        date_mise_en_vigueur = datetime.strptime(row[20], "%Y/%m/%d").date() if row[20] else None
        champ_inutilise_38 = row[21] if row[21] else None
        mun_code = get_id_municipalite(row[22])
        quartr_code = get_id_quartiers(row[23], mun_code)
        pres_de = row[24] if row[24] else None
        no_civique_debut = row[25] if row[25] else None
        no_civique_fin = row[26] if row[26] else None
        nom_rue_complet = row[27] if row[27] else None
        appartement = row[28] if row[28] else None
        code_postal = row[29] if row[29] else None
        champ_inutilise_39 = row[30] if row[30] else None
        champ_inutilise_40 = row[31] if row[31] else None
        champ_inutilise_41 = row[32] if row[32] else None
        champ_inutilise_5 = row[33] if row[33] else None
        champ_inutilise_6 = row[34] if row[34] else None
        champ_inutilise_7 = row[35] if row[35] else None
        champ_inutilise_8 = row[36] if row[36] else None
        champ_inutilise_9 = row[37] if row[37] else None
        champ_inutilise_10 = row[38] if row[38] else None
        champ_inutilise_11 = row[39] if row[39] else None
        champ_inutilise_12 = row[40] if row[40] else None
        champ_inutilise_13 = row[41] if row[41] else None
        champ_inutilise_14 = row[42] if row[42] else None
        date_occupation = datetime.strptime(row[43], "%Y/%m/%d").date() if row[43] else None
        delai_occupation_francais = row[44] if row[44] else None
        delai_occupation_anglais = row[45] if row[45] else None
        champ_inutilise_42 = row[46] if row[46] else None
        champ_inutilise_43 = row[47] if row[47] else None
        champ_inutilise_44 = row[48] if row[48] else None
        date_fin_bail = datetime.strptime(row[49], "%Y/%m/%d").date() if row[49] else None
        champ_inutilise_52 = row[50] if row[50] else None
        champ_inutilise_15 = row[51] if row[51] else None
        champ_inutilise_45 = row[52] if row[52] else None
        valor_valeurs_fixes = row[53]
        categorie_propriete = get_id_valeurs(valor_valeurs_fixes,'CATEGORIE_PROPRIETE')
        genre_propriete = get_id_genres_proprietes(row[54])
        valor_valeurs_fixes = row[55]
        type_batiment = get_id_valeurs(valor_valeurs_fixes,'TYPE_BATIMENT')
        valor_valeurs_fixes = row[56]
        type_copropriete = get_id_valeurs(valor_valeurs_fixes,'TYPE_COPROPRIETE')
        valor_valeurs_fixes = row[57]
        niveau = get_id_valeurs(valor_valeurs_fixes,'NIVEAU')
        nb_etages = int(row[58]) if row[58] else None
        annee_contruction = row[59] if row[59] else None
        code_annee_construction = row[60] if row[60] else None
        champ_inutilise_16 = row[61] if row[61] else None
        facade_batiment = float(row[62]) if row[62] else None
        profondeur_batiment = float(row[63]) if row[63] else None
        ind_irregulier_batiment = row[64] if row[64] else None
        valor_valeurs_fixes = row[65]
        um_dimension_batiment = get_id_valeurs(valor_valeurs_fixes,'UM_DIMENSION_BATIMEN')
        superficie_batiment = float(row[66]) if row[66] else None
        valor_valeurs_fixes = row[67]
        um_superficie_batiment = get_id_valeurs(valor_valeurs_fixes,'UM_DIMENSION_BATIMEN')
        superficie_habitable = float(row[68]) if row[68] else None
        valor_valeurs_fixes = row[69]
        um_superficie_habitable = get_id_valeurs(valor_valeurs_fixes,'UM_AIRE_BATIMENT')
        champ_inutilise_17 = row[70] if row[70] else None
        facade_terrain = float(row[71]) if row[71] else None
        profondeur_terrain = float(row[72]) if row[72] else None
        ind_irregulier_terrain = row[73] if row[73] else None
        valor_valeurs_fixes = row[74]
        um_dimension_terrain = get_id_valeurs(valor_valeurs_fixes,'UM_DIMENSION_TERRAIN')
        superficie_terrain = float(row[75]) if row[75] else None
        valor_valeurs_fixes = row[76]
        um_superficie_terrain = get_id_valeurs(valor_valeurs_fixes,'UM_SUPERFICIE_TERRAIN')
        champ_inutilise_46 = row[77] if row[77] else None
        annee_evaluation = row[78] if row[78] else None
        evaluation_municipale_terrain = int(row[79]) if row[79] else None
        evaluation_municipale_batiment = int(row[80]) if row[80] else None
        nb_pieces = int(row[81]) if row[81] else None
        nb_chambres = int(row[82]) if row[82] else None
        nb_chambres_sous_sol = int(row[83]) if row[83] else None
        nb_chambres_hors_sol = int(row[84]) if row[84] else None
        nb_salles_bains = float(row[85]) if row[85] else None
        nb_salles_eau = int(row[86]) if row[86] else None
        champ_inutilise_47 = row[87] if row[87] else None
        champ_inutilise_48 = row[88] if row[88] else None
        champ_inutilise_18 = row[89] if row[89] else None
        champ_inutilise_19 = row[90] if row[90] else None
        champ_inutilise_20 = row[91] if row[91] else None
        champ_inutilise_21 = row[92] if row[92] else None
        depenses_tot_exploitation = int(row[93]) if row[93] else None
        champ_inutilise_22 = row[94] if row[94] else None
        champ_inutilise_23 = row[95] if row[95] else None
        nom_plan_eau = row[96] if row[96] else None
        champ_inutilise_24 = row[97] if row[97] else None
        champ_inutilise_25 = row[98] if row[98] else None
        nb_chauffe_eau_loue = int(row[99]) if row[99] else None
        inclus_francais = row[100] if row[100] else None
        inclus_anglais = row[101] if row[101] else None
        exclus_francais = row[102] if row[102] else None
        exclus_anglais = row[103] if row[103] else None
        nb_unites_total = int(row[104]) if row[104] else None
        champ_inutilise_26 = row[105] if row[105] else None
        champ_inutilise_27 = row[106] if row[106] else None
        champ_inutilise_28 = row[107] if row[107] else None
        champ_inutilise_29 = row[108] if row[108] else None
        champ_inutilise_30 = row[109] if row[109] else None
        champ_inutilise_31 = row[110] if row[110] else None
        champ_inutilise_32 = row[111] if row[111] else None
        champ_inutilise_49 = row[112] if row[112] else None
        date_modif = timezone.make_aware(datetime.strptime(row[113], "%Y/%m/%d %H:%M:%S")) if row[113] else None
        valor_valeurs_fixes = row[114]
        frequence_prix_location = get_id_valeurs(valor_valeurs_fixes,'FREQUENCE_PRIX_LOCATION')
        valor_valeurs_fixes = row[115]
        code_statut = get_id_valeurs(valor_valeurs_fixes,'CODE_STATUT')
        pourc_quote_part = float(row[116]) if row[116] else None
        valor_valeurs_fixes = row[117]
        utilisation_commerciale = get_id_valeurs(valor_valeurs_fixes,'UTILISATION_COMMERCIALE')
        champ_inutilise_2 = row[118] if row[118] else None
        nom_du_parc = row[119] if row[119] else None
        champ_inutilise_50 = row[120] if row[120] else None
        champ_inutilise_51 = row[121] if row[121] else None
        raison_sociale = row[122] if row[122] else None
        en_oper_depuis = row[123] if row[123] else None
        ind_franchise = row[124] if row[124] else None
        champ_inutilise_33 = row[125] if row[125] else None
        champ_inutilise_34 = row[126] if row[126] else None
        champ_inutilise_35 = row[127] if row[127] else None
        ind_opt_renouv_bail = row[128] if row[128] else None
        annee_mois_echeance_bail = row[129] if row[129] else None
        url_visite_virtuelle_francais = row[130] if row[130] else None
        url_visite_virtuelle_anglais = row[131] if row[131] else None
        url_desc_detaillee = row[132] if row[132] else None
        ind_taxes_prix_demande = row[133] if row[133] else None
        ind_taxes_prix_location_demande = row[134] if row[134] else None
        courtier_inscripteur_3 = row[135] if row[135] else None
        bureau_inscripteur_3 = row[136] if row[136] else None
        courtier_inscripteur_4 = row[137] if row[137] else None
        bureau_inscripteur_4 = row[138] if row[138] else None
        valor_valeurs_fixes = row[139]
        courtier1_type_divul_interet = get_id_valeurs(valor_valeurs_fixes,'TYPE_DIVUL_INTERET')
        valor_valeurs_fixes = row[140]
        courtier2_type_divul_interet = get_id_valeurs(valor_valeurs_fixes,'TYPE_DIVUL_INTERET')
        valor_valeurs_fixes = row[141]
        courtier3_type_divul_interet = get_id_valeurs(valor_valeurs_fixes,'TYPE_DIVUL_INTERET')
        valor_valeurs_fixes = row[142]
        courtier4_type_divul_interet = get_id_valeurs(valor_valeurs_fixes,'TYPE_DIVUL_INTERET')
        valor_valeurs_fixes = row[143]
        ind_vente_sans_garantie_legale = get_id_valeurs(valor_valeurs_fixes,'IND_VENTE_SANS_GARANTIE_LEGALE')
        latitude = float(row[144]) if row[144] else None
        longitude = float(row[145]) if row[145] else None
        valor_valeurs_fixes = row[146]
        type_superficie_habitable = get_id_valeurs(valor_valeurs_fixes,'TYPE_SUPERFICIE_HABITABLE')
        rev_pot_brut_res = int(row[147]) if row[147] else None
        rev_pot_brut_comm = int(row[148]) if row[148] else None
        rev_pot_brut_stat = int(row[149]) if row[149] else None
        rev_pot_brut_au = int(row[150]) if row[150] else None
        date_rev_brut_pot = datetime.strptime(row[151], "%Y/%m/%d").date() if row[151] else None
        valor_valeurs_fixes = row[152]
        particularite_construction = get_id_valeurs(valor_valeurs_fixes,'PARTICULARITE_CONSTRUCTION')
        au_genre_propriete_info_f = row[153] if row[153] else None
        au_genre_propriete_info_a = row[154] if row[154] else None
        prix_demande_taxe_incl = row[155] if row[155] else None
        ind_visites_interactive = row[156] if row[156] else None
        addenda_complet_f = row[157] if row[157] else None
        addenda_complet_a = row[158] if row[158] else None

        try:
            inscription = Inscriptions.objects.get(no_inscription = no_inscription)

            cambios = []
            if inscription.champ_inutilise_1 != champ_inutilise_1:
                inscription.champ_inutilise_1 = champ_inutilise_1
                cambios.append('champ_inutilise_1')
            if inscription.courtier_inscripteur_1 != courtier_inscripteur_1:
                inscription.courtier_inscripteur_1 = courtier_inscripteur_1
                cambios.append('courtier_inscripteur_1')
            if inscription.bureau_inscripteur_1 != bureau_inscripteur_1:
                inscription.bureau_inscripteur_1 = bureau_inscripteur_1
                cambios.append('bureau_inscripteur_1')
            if inscription.courtier_inscripteur_2 != courtier_inscripteur_2:
                inscription.courtier_inscripteur_2 = courtier_inscripteur_2
                cambios.append('courtier_inscripteur_2')
            if inscription.bureau_inscripteur_2 != bureau_inscripteur_2:
                inscription.bureau_inscripteur_2 = bureau_inscripteur_2
                cambios.append('bureau_inscripteur_2')
            if inscription.prix_demande != prix_demande:
                inscription.prix_demande = prix_demande
                cambios.append(no_inscription)
                cambios.append('prix_demande')
            if inscription.um_prix_demande != um_prix_demande:
                inscription.um_prix_demande = um_prix_demande
                cambios.append('um_prix_demande')
            if inscription.devise_prix_demande != devise_prix_demande:
                inscription.devise_prix_demande = devise_prix_demande
                cambios.append('devise_prix_demande')
            if inscription.prix_location_demande != prix_location_demande:
                inscription.prix_location_demande = prix_location_demande
                cambios.append('prix_location_demande')
            if inscription.um_prix_location_demande != um_prix_location_demande:
                inscription.um_prix_location_demande = um_prix_location_demande
                cambios.append('um_prix_location_demande')
            if inscription.devise_prix_location_demande != devise_prix_location_demande:
                inscription.devise_prix_location_demande = devise_prix_location_demande
                cambios.append('devise_prix_location_demande')
            if inscription.champ_inutilise_36 != champ_inutilise_36:
                inscription.champ_inutilise_36 = champ_inutilise_36
                cambios.append('champ_inutilise_36')
            if inscription.code_declaration_vendeur != code_declaration_vendeur:
                inscription.code_declaration_vendeur = code_declaration_vendeur
                cambios.append('code_declaration_vendeur')
            if inscription.ind_reprise_finance != ind_reprise_finance:
                inscription.ind_reprise_finance = ind_reprise_finance
                cambios.append('ind_reprise_finance')
            if inscription.ind_internet != ind_internet:
                inscription.ind_internet = ind_internet
                cambios.append('ind_internet')
            if inscription.ind_echange_possible != ind_echange_possible:
                inscription.ind_echange_possible = ind_echange_possible
                cambios.append('ind_echange_possible')
            if inscription.champ_inutilise_37 != champ_inutilise_37:
                inscription.champ_inutilise_37 = champ_inutilise_37
                cambios.append('champ_inutilise_37')
            if inscription.champ_inutilise_3 != champ_inutilise_3:
                inscription.champ_inutilise_3 = champ_inutilise_3
                cambios.append('champ_inutilise_3')
            if inscription.champ_inutilise_4 != champ_inutilise_4:
                inscription.champ_inutilise_4 =  champ_inutilise_4
                cambios.append('champ_inutilise_4')
            if inscription.date_mise_en_vigueur != date_mise_en_vigueur:
                inscription.date_mise_en_vigueur = date_mise_en_vigueur
                cambios.append('date_mise_en_vigueur')
            if inscription.champ_inutilise_38 != champ_inutilise_38:
                inscription.champ_inutilise_38 = champ_inutilise_38
                cambios.append('champ_inutilise_38')
            if inscription.mun_code != mun_code:
                inscription.mun_code = mun_code
                cambios.append('mun_code')
            if inscription.quartr_code != quartr_code:
                inscription.quartr_code = quartr_code
                cambios.append('quartr_code')
            if inscription.pres_de != pres_de:
                inscription.pres_de = pres_de
                cambios.append('pres_de')
            if inscription.no_civique_debut != no_civique_debut:
                inscription.no_civique_debut = no_civique_debut
                cambios.append('no_civique_debut')
            if inscription.no_civique_fin != no_civique_fin:
                inscription.no_civique_fin = no_civique_fin
                cambios.append('no_civique_fin')
            if inscription.nom_rue_complet != nom_rue_complet:
                inscription.nom_rue_complet = nom_rue_complet
                cambios.append('nom_rue_complet')
            if inscription.appartement != appartement:
                inscription.appartement = appartement
                cambios.append('appartement')
            if inscription.code_postal != code_postal:
                inscription.code_postal = code_postal
                cambios.append('code_postal')
            if inscription.champ_inutilise_39 != champ_inutilise_39:
                inscription.champ_inutilise_39 = champ_inutilise_39
                cambios.append('champ_inutilise_39')
            if inscription.champ_inutilise_40 != champ_inutilise_40:
                inscription.champ_inutilise_40 = champ_inutilise_40
                cambios.append('champ_inutilise_40')
            if inscription.champ_inutilise_41 != champ_inutilise_41:
                inscription.champ_inutilise_41 = champ_inutilise_41
                cambios.append('champ_inutilise_41')
            if inscription.champ_inutilise_5 != champ_inutilise_5:
                inscription.champ_inutilise_5 = champ_inutilise_5
                cambios.append('champ_inutilise_5')
            if inscription.champ_inutilise_6 != champ_inutilise_6:
                inscription.champ_inutilise_6 = champ_inutilise_6
                cambios.append('champ_inutilise_6')
            if inscription.champ_inutilise_7 != champ_inutilise_7:
                inscription.champ_inutilise_7 = champ_inutilise_7
                cambios.append('champ_inutilise_7')
            if inscription.champ_inutilise_8 != champ_inutilise_8:
                inscription.champ_inutilise_8 = champ_inutilise_8
                cambios.append('champ_inutilise_8')
            if inscription.champ_inutilise_9 != champ_inutilise_9:
                inscription.champ_inutilise_9 = champ_inutilise_9
                cambios.append('champ_inutilise_9')
            if inscription.champ_inutilise_10 != champ_inutilise_10:
                inscription.champ_inutilise_10 = champ_inutilise_10
                cambios.append('champ_inutilise_10')
            if inscription.champ_inutilise_11 != champ_inutilise_11:
                inscription.champ_inutilise_11 = champ_inutilise_11
                cambios.append('champ_inutilise_11')
            if inscription.champ_inutilise_12 != champ_inutilise_12:
                inscription.champ_inutilise_12 = champ_inutilise_12
                cambios.append('champ_inutilise_12')
            if inscription.champ_inutilise_13 != champ_inutilise_13:
                inscription.champ_inutilise_13 = champ_inutilise_13
                cambios.append('champ_inutilise_13')
            if inscription.champ_inutilise_14 != champ_inutilise_14:
                inscription.champ_inutilise_14 = champ_inutilise_14
                cambios.append('champ_inutilise_14')
            if inscription.date_occupation != date_occupation:
                inscription.date_occupation = date_occupation
                cambios.append('date_occupation')
            if inscription.delai_occupation_francais != delai_occupation_francais:
                inscription.delai_occupation_francais = delai_occupation_francais
                cambios.append('delai_occupation_francais')
            if inscription.delai_occupation_anglais != delai_occupation_anglais:
                inscription.delai_occupation_anglais = delai_occupation_anglais
                cambios.append('delai_occupation_anglais')
            if inscription.champ_inutilise_42 != champ_inutilise_42:
                inscription.champ_inutilise_42 = champ_inutilise_42
                cambios.append('champ_inutilise_42')
            if inscription.champ_inutilise_43 != champ_inutilise_43:
                inscription.champ_inutilise_43 = champ_inutilise_43
                cambios.append('champ_inutilise_43')
            if inscription.champ_inutilise_44 != champ_inutilise_44:
                inscription.champ_inutilise_44 = champ_inutilise_44
                cambios.append('champ_inutilise_44')
            if inscription.date_fin_bail != date_fin_bail:
                inscription.date_fin_bail = date_fin_bail
                cambios.append('date_fin_bail')
            if inscription.champ_inutilise_52 != champ_inutilise_52:
                inscription.champ_inutilise_52 = champ_inutilise_52
                cambios.append('champ_inutilise_52')
            if inscription.champ_inutilise_15 != champ_inutilise_15:
                inscription.champ_inutilise_15 = champ_inutilise_15
                cambios.append('champ_inutilise_15')
            if inscription.champ_inutilise_45 != champ_inutilise_45:
                inscription.champ_inutilise_45 = champ_inutilise_45
                cambios.append('champ_inutilise_45')
            if inscription.categorie_propriete != categorie_propriete:
                inscription.categorie_propriete = categorie_propriete
                cambios.append('categorie_propriete')
            if inscription.genre_propriete != genre_propriete:
                inscription.genre_propriete = genre_propriete
                cambios.append('genre_propriete')
            if inscription.type_batiment != type_batiment:
                inscription.type_batiment = type_batiment
                cambios.append('type_batiment')
            if inscription.type_copropriete != type_copropriete:
                inscription.type_copropriete = type_copropriete
                cambios.append('type_copropriete')
            if inscription.niveau != niveau:
                inscription.niveau = niveau
                cambios.append('niveau')
            if inscription.nb_etages != nb_etages:
                inscription.nb_etages = nb_etages
                cambios.append('nb_etages')
            if inscription.annee_contruction != annee_contruction:
                inscription.annee_contruction = annee_contruction
                cambios.append('annee_contruction')
            if inscription.code_annee_construction != code_annee_construction:
                inscription.code_annee_construction = code_annee_construction
                cambios.append('code_annee_construction')
            if inscription.champ_inutilise_16 != champ_inutilise_16:
                inscription.champ_inutilise_16 = champ_inutilise_16
                cambios.append('champ_inutilise_16')
            if inscription.facade_batiment != facade_batiment:
                inscription.facade_batiment = facade_batiment
                cambios.append('facade_batiment')
            if inscription.profondeur_batiment != profondeur_batiment:
                inscription.profondeur_batiment = profondeur_batiment
                cambios.append('profondeur_batiment')
            if inscription.ind_irregulier_batiment != ind_irregulier_batiment:
                inscription.ind_irregulier_batiment = ind_irregulier_batiment
                cambios.append('ind_irregulier_batiment')
            if inscription.um_dimension_batiment != um_dimension_batiment:
                inscription.um_dimension_batiment = um_dimension_batiment
                cambios.append('um_dimension_batiment')
            if inscription.superficie_batiment != superficie_batiment:
                inscription.superficie_batiment = superficie_batiment
                cambios.append('superficie_batiment')
            if inscription.um_superficie_batiment != um_superficie_batiment:
                inscription.um_superficie_batiment = um_superficie_batiment
                cambios.append('um_superficie_batiment')
            if inscription.superficie_habitable != superficie_habitable:
                inscription.superficie_habitable = superficie_habitable
                cambios.append('superficie_habitable')
            if inscription.um_superficie_habitable != um_superficie_habitable:
                inscription.um_superficie_habitable = um_superficie_habitable
                cambios.append('um_superficie_habitable')
            if inscription.champ_inutilise_17 != champ_inutilise_17:
                inscription.champ_inutilise_17 = champ_inutilise_17
                cambios.append('champ_inutilise_17')
            if inscription.facade_terrain != facade_terrain:
                inscription.facade_terrain = facade_terrain
                cambios.append('facade_terrain')
            if inscription.profondeur_terrain != profondeur_terrain:
                inscription.profondeur_terrain = profondeur_terrain
                cambios.append('profondeur_terrain')
            if inscription.ind_irregulier_terrain != ind_irregulier_terrain:
                inscription.ind_irregulier_terrain = ind_irregulier_terrain
                cambios.append('ind_irregulier_terrain')
            if inscription.um_dimension_terrain != um_dimension_terrain:
                inscription.um_dimension_terrain = um_dimension_terrain
                cambios.append('um_dimension_terrain')
            if inscription.superficie_terrain != superficie_terrain:
                inscription.superficie_terrain = superficie_terrain
                cambios.append('superficie_terrain')
            if inscription.um_superficie_terrain != um_superficie_terrain:
                inscription.um_superficie_terrain = um_superficie_terrain
                cambios.append('um_superficie_terrain')
            if inscription.champ_inutilise_46 != champ_inutilise_46:
                inscription.champ_inutilise_46 = champ_inutilise_46
                cambios.append('champ_inutilise_46')
            if inscription.annee_evaluation != annee_evaluation:
                inscription.annee_evaluation = annee_evaluation
                cambios.append('annee_evaluation')
            if inscription.evaluation_municipale_terrain != evaluation_municipale_terrain:
                inscription.evaluation_municipale_terrain = evaluation_municipale_terrain
                cambios.append('evaluation_municipale_terrain')
            if inscription.evaluation_municipale_batiment != evaluation_municipale_batiment:
                inscription.evaluation_municipale_batiment = evaluation_municipale_batiment
                cambios.append('evaluation_municipale_batiment')
            if inscription.nb_pieces != nb_pieces:
                inscription.nb_pieces = nb_pieces
                cambios.append('nb_pieces')
            if inscription.nb_chambres != nb_chambres:
                inscription.nb_chambres = nb_chambres
                cambios.append('nb_chambres')
            if inscription.nb_chambres_sous_sol != nb_chambres_sous_sol:
                inscription.nb_chambres_sous_sol = nb_chambres_sous_sol
                cambios.append('nb_chambres_sous_sol')
            if inscription.nb_chambres_hors_sol != nb_chambres_hors_sol:
                inscription.nb_chambres_hors_sol = nb_chambres_hors_sol
                cambios.append('nb_chambres_hors_sol')
            if inscription.nb_salles_bains != nb_salles_bains:
                inscription.nb_salles_bains = nb_salles_bains
                cambios.append('nb_salles_bains')
            if inscription.nb_salles_eau != nb_salles_eau:
                inscription.nb_salles_eau = nb_salles_eau
                cambios.append('nb_salles_eau')
            if inscription.champ_inutilise_47 != champ_inutilise_47:
                inscription.champ_inutilise_47 = champ_inutilise_47
                cambios.append('champ_inutilise_47')
            if inscription.champ_inutilise_48 != champ_inutilise_48:
                inscription.champ_inutilise_48 = champ_inutilise_48
                cambios.append('champ_inutilise_48')
            if inscription.champ_inutilise_18 != champ_inutilise_18:
                inscription.champ_inutilise_18 = champ_inutilise_18
                cambios.append('champ_inutilise_18')
            if inscription.champ_inutilise_19 != champ_inutilise_19:
                inscription.champ_inutilise_19 = champ_inutilise_19
                cambios.append('champ_inutilise_19')
            if inscription.champ_inutilise_20 != champ_inutilise_20:
                inscription.champ_inutilise_20 = champ_inutilise_20
                cambios.append('champ_inutilise_20')
            if inscription.champ_inutilise_21 != champ_inutilise_21:
                inscription.champ_inutilise_21 = champ_inutilise_21
                cambios.append('champ_inutilise_21')
            if inscription.depenses_tot_exploitation != depenses_tot_exploitation:
                inscription.depenses_tot_exploitation = depenses_tot_exploitation
                cambios.append('depenses_tot_exploitation')
            if inscription.champ_inutilise_22 != champ_inutilise_22:
                inscription.champ_inutilise_22 = champ_inutilise_22
                cambios.append('champ_inutilise_22')
            if inscription.champ_inutilise_23 != champ_inutilise_23:
                inscription.champ_inutilise_23 = champ_inutilise_23
                cambios.append('champ_inutilise_23')
            if inscription.nom_plan_eau != nom_plan_eau:
                inscription.nom_plan_eau = nom_plan_eau
                cambios.append('nom_plan_eau')
            if inscription.champ_inutilise_24 != champ_inutilise_24:
                inscription.champ_inutilise_24 = champ_inutilise_24
                cambios.append('champ_inutilise_24')
            if inscription.champ_inutilise_25 != champ_inutilise_25:
                inscription.champ_inutilise_25 = champ_inutilise_25
                cambios.append('champ_inutilise_25')
            if inscription.nb_chauffe_eau_loue != nb_chauffe_eau_loue:
                inscription.nb_chauffe_eau_loue = nb_chauffe_eau_loue
                cambios.append('nb_chauffe_eau_loue')
            if inscription.inclus_francais != inclus_francais:
                inscription.inclus_francais = inclus_francais
                cambios.append('inclus_francais')
            if inscription.inclus_anglais != inclus_anglais:
                inscription.inclus_anglais = inclus_anglais
                cambios.append('inclus_anglais')
            if inscription.exclus_francais != exclus_francais:
                inscription.exclus_francais = exclus_francais
                cambios.append('exclus_francais')
            if inscription.exclus_anglais != exclus_anglais:
                inscription.exclus_anglais = exclus_anglais
                cambios.append('exclus_anglais')
            if inscription.nb_unites_total != nb_unites_total:
                inscription.nb_unites_total = nb_unites_total
                cambios.append('nb_unites_total')
            if inscription.champ_inutilise_26 != champ_inutilise_26:
                inscription.champ_inutilise_26 = champ_inutilise_26
                cambios.append('champ_inutilise_26')
            if inscription.champ_inutilise_27 != champ_inutilise_27:
                inscription.champ_inutilise_27 = champ_inutilise_27
                cambios.append('champ_inutilise_27')
            if inscription.champ_inutilise_28 != champ_inutilise_28:
                inscription.champ_inutilise_28 = champ_inutilise_28
                cambios.append('champ_inutilise_28')
            if inscription.champ_inutilise_29 != champ_inutilise_29:
                inscription.champ_inutilise_29 = champ_inutilise_29
                cambios.append('champ_inutilise_29')
            if inscription.champ_inutilise_30 != champ_inutilise_30:
                inscription.champ_inutilise_30 = champ_inutilise_30
                cambios.append('champ_inutilise_30')
            if inscription.champ_inutilise_31 != champ_inutilise_31:
                inscription.champ_inutilise_31 = champ_inutilise_31
                cambios.append('champ_inutilise_31')
            if inscription.champ_inutilise_32 != champ_inutilise_32:
                inscription.champ_inutilise_32 = champ_inutilise_32
                cambios.append('champ_inutilise_32')
            if inscription.champ_inutilise_49 != champ_inutilise_49:
                inscription.champ_inutilise_49 = champ_inutilise_49
                cambios.append('champ_inutilise_49')
            if inscription.date_modif != date_modif:
                inscription.date_modif = date_modif
                cambios.append('date_modif')
            if inscription.frequence_prix_location != frequence_prix_location:
                inscription.frequence_prix_location = frequence_prix_location
                cambios.append('frequence_prix_location')
            if inscription.code_statut != code_statut:
                inscription.code_statut = code_statut
                cambios.append('code_statut')
            if inscription.pourc_quote_part != pourc_quote_part:
                inscription.pourc_quote_part = pourc_quote_part
                cambios.append('pourc_quote_part')
            if inscription.utilisation_commerciale != utilisation_commerciale:
                inscription.utilisation_commerciale = utilisation_commerciale
                cambios.append('utilisation_commerciale')
            if inscription.champ_inutilise_2 != champ_inutilise_2:
                inscription.champ_inutilise_2 = champ_inutilise_2
                cambios.append('champ_inutilise_2')
            if inscription.nom_du_parc != nom_du_parc:
                inscription.nom_du_parc = nom_du_parc
                cambios.append('nom_du_parc')
            if inscription.champ_inutilise_50 != champ_inutilise_50:
                inscription.champ_inutilise_50 = champ_inutilise_50
                cambios.append('champ_inutilise_50')
            if inscription.champ_inutilise_51 != champ_inutilise_51:
                inscription.champ_inutilise_51 = champ_inutilise_51
                cambios.append('champ_inutilise_51')
            if inscription.raison_sociale != raison_sociale:
                inscription.raison_sociale = raison_sociale
                cambios.append('raison_sociale')
            if inscription.en_oper_depuis != en_oper_depuis:
                inscription.en_oper_depuis = en_oper_depuis
                cambios.append('en_oper_depuis')
            if inscription.ind_franchise != ind_franchise:
                inscription.ind_franchise = ind_franchise
                cambios.append('ind_franchise')
            if inscription.champ_inutilise_33 != champ_inutilise_33:
                inscription.champ_inutilise_33 = champ_inutilise_33
                cambios.append('champ_inutilise_33')
            if inscription.champ_inutilise_34 != champ_inutilise_34:
                inscription.champ_inutilise_34 = champ_inutilise_34
                cambios.append('champ_inutilise_34')
            if inscription.champ_inutilise_35 != champ_inutilise_35:
                inscription.champ_inutilise_35 = champ_inutilise_35
                cambios.append('champ_inutilise_35')
            if inscription.ind_opt_renouv_bail != ind_opt_renouv_bail:
                inscription.ind_opt_renouv_bail = ind_opt_renouv_bail
                cambios.append('ind_opt_renouv_bail')
            if inscription.annee_mois_echeance_bail != annee_mois_echeance_bail:
                inscription.annee_mois_echeance_bail = annee_mois_echeance_bail
                cambios.append('annee_mois_echeance_bail')
            if inscription.url_visite_virtuelle_francais != url_visite_virtuelle_francais:
                inscription.url_visite_virtuelle_francais = url_visite_virtuelle_francais
                cambios.append('url_visite_virtuelle_francais')
            if inscription.url_visite_virtuelle_anglais != url_visite_virtuelle_anglais:
                inscription.url_visite_virtuelle_anglais = url_visite_virtuelle_anglais
                cambios.append('url_visite_virtuelle_anglais')
            if inscription.url_desc_detaillee != url_desc_detaillee:
                inscription.url_desc_detaillee = url_desc_detaillee
                cambios.append('url_desc_detaillee')
            if inscription.ind_taxes_prix_demande != ind_taxes_prix_demande:
                inscription.ind_taxes_prix_demande = ind_taxes_prix_demande
                cambios.append('ind_taxes_prix_demande')
            if inscription.ind_taxes_prix_location_demande != ind_taxes_prix_location_demande:
                inscription.ind_taxes_prix_location_demande = ind_taxes_prix_location_demande
                cambios.append('ind_taxes_prix_location_demande')
            if inscription.courtier_inscripteur_3 != courtier_inscripteur_3:
                inscription.courtier_inscripteur_3 = courtier_inscripteur_3
                cambios.append('courtier_inscripteur_3')
            if inscription.bureau_inscripteur_3 != bureau_inscripteur_3:
                inscription.bureau_inscripteur_3 = bureau_inscripteur_3
                cambios.append('bureau_inscripteur_3')
            if inscription.courtier_inscripteur_4 != courtier_inscripteur_4:
                inscription.courtier_inscripteur_4 = courtier_inscripteur_4
                cambios.append('courtier_inscripteur_4')
            if inscription.bureau_inscripteur_4 != bureau_inscripteur_4:
                inscription.bureau_inscripteur_4 = bureau_inscripteur_4
                cambios.append('bureau_inscripteur_4')
            if inscription.courtier1_type_divul_interet != courtier1_type_divul_interet:
                inscription.courtier1_type_divul_interet = courtier1_type_divul_interet
                cambios.append('courtier1_type_divul_interet')
            if inscription.courtier2_type_divul_interet != courtier2_type_divul_interet:
                inscription.courtier2_type_divul_interet = courtier2_type_divul_interet
                cambios.append('courtier2_type_divul_interet')
            if inscription.courtier3_type_divul_interet != courtier3_type_divul_interet:
                inscription.courtier3_type_divul_interet = courtier3_type_divul_interet
                cambios.append('courtier3_type_divul_interet')
            if inscription.courtier4_type_divul_interet != courtier4_type_divul_interet:
                inscription.courtier4_type_divul_interet = courtier4_type_divul_interet
                cambios.append('courtier4_type_divul_interet')
            if inscription.ind_vente_sans_garantie_legale != ind_vente_sans_garantie_legale:
                inscription.ind_vente_sans_garantie_legale = ind_vente_sans_garantie_legale
                cambios.append('ind_vente_sans_garantie_legale')
            if inscription.latitude != latitude:
                inscription.latitude = latitude
                cambios.append('latitude')
            if inscription.longitude != longitude:
                inscription.longitude = longitude
                cambios.append('longitude')
            if inscription.type_superficie_habitable != type_superficie_habitable:
                inscription.type_superficie_habitable = type_superficie_habitable
                cambios.append('type_superficie_habitable')
            if inscription.rev_pot_brut_res != rev_pot_brut_res:
                inscription.rev_pot_brut_res = rev_pot_brut_res
                cambios.append('rev_pot_brut_res')
            if inscription.rev_pot_brut_comm != rev_pot_brut_comm:
                inscription.rev_pot_brut_comm = rev_pot_brut_comm
                cambios.append('rev_pot_brut_comm')
            if inscription.rev_pot_brut_stat != rev_pot_brut_stat:
                inscription.rev_pot_brut_stat = rev_pot_brut_stat
                cambios.append('rev_pot_brut_stat')
            if inscription.rev_pot_brut_au != rev_pot_brut_au:
                inscription.rev_pot_brut_au = rev_pot_brut_au
                cambios.append('rev_pot_brut_au')
            if inscription.date_rev_brut_pot != date_rev_brut_pot:
                inscription.date_rev_brut_pot = date_rev_brut_pot
                cambios.append('date_rev_brut_pot')
            if inscription.particularite_construction != particularite_construction:
                inscription.particularite_construction = particularite_construction
                cambios.append('particularite_construction')
            if inscription.au_genre_propriete_info_f != au_genre_propriete_info_f:
                inscription.au_genre_propriete_info_f = au_genre_propriete_info_f
                cambios.append('au_genre_propriete_info_f')
            if inscription.au_genre_propriete_info_a != au_genre_propriete_info_a:
                inscription.au_genre_propriete_info_a = au_genre_propriete_info_a
                cambios.append('au_genre_propriete_info_a')
            if inscription.prix_demande_taxe_incl != prix_demande_taxe_incl:
                inscription.prix_demande_taxe_incl = prix_demande_taxe_incl
                cambios.append('prix_demande_taxe_incl')
            if inscription.ind_visites_interactive != ind_visites_interactive:
                inscription.ind_visites_interactive = ind_visites_interactive
                cambios.append('ind_visites_interactive')
            if inscription.addenda_complet_f != addenda_complet_f:
                inscription.addenda_complet_f = addenda_complet_f
                cambios.append('addenda_complet_f')
            if inscription.addenda_complet_a != addenda_complet_a:
                inscription.addenda_complet_a = addenda_complet_a
                cambios.append('addenda_complet_a')

            if cambios:
                print(cambios)
                inscription.save()
                total_actualizadas = total_actualizadas + 1

        except ObjectDoesNotExist:

            inscription = Inscriptions.objects.create(
                no_inscription = no_inscription,
                champ_inutilise_1 = champ_inutilise_1,
                courtier_inscripteur_1 = courtier_inscripteur_1,
                bureau_inscripteur_1 = bureau_inscripteur_1,
                courtier_inscripteur_2 = courtier_inscripteur_2,
                bureau_inscripteur_2 = bureau_inscripteur_2,
                prix_demande = prix_demande,
                um_prix_demande = um_prix_demande,
                devise_prix_demande = devise_prix_demande,
                prix_location_demande = prix_location_demande,
                um_prix_location_demande = um_prix_location_demande,
                devise_prix_location_demande = devise_prix_location_demande,
                champ_inutilise_36 = champ_inutilise_36,
                code_declaration_vendeur = code_declaration_vendeur,
                ind_reprise_finance = ind_reprise_finance,
                ind_internet = ind_internet,
                ind_echange_possible = ind_echange_possible,
                champ_inutilise_37 = champ_inutilise_37,
                champ_inutilise_3 = champ_inutilise_3,
                champ_inutilise_4 = champ_inutilise_4,
                date_mise_en_vigueur = date_mise_en_vigueur,
                champ_inutilise_38 = champ_inutilise_38,
                mun_code = mun_code,
                quartr_code = quartr_code,
                pres_de = pres_de,
                no_civique_debut = no_civique_debut,
                no_civique_fin = no_civique_fin,
                nom_rue_complet = nom_rue_complet,
                appartement = appartement,
                code_postal = code_postal,
                champ_inutilise_39 = champ_inutilise_39,
                champ_inutilise_40 = champ_inutilise_40,
                champ_inutilise_41 = champ_inutilise_41,
                champ_inutilise_5 = champ_inutilise_5,
                champ_inutilise_6 = champ_inutilise_6,
                champ_inutilise_7 = champ_inutilise_7,
                champ_inutilise_8 = champ_inutilise_8,
                champ_inutilise_9 = champ_inutilise_9,
                champ_inutilise_10 = champ_inutilise_10,
                champ_inutilise_11 = champ_inutilise_11,
                champ_inutilise_12 = champ_inutilise_12,
                champ_inutilise_13 = champ_inutilise_13,
                champ_inutilise_14 = champ_inutilise_14,
                date_occupation = date_occupation,
                delai_occupation_francais = delai_occupation_francais,
                delai_occupation_anglais = delai_occupation_anglais,
                champ_inutilise_42 = champ_inutilise_42,
                champ_inutilise_43 = champ_inutilise_43,
                champ_inutilise_44 = champ_inutilise_44,
                date_fin_bail = date_fin_bail,
                champ_inutilise_52 = champ_inutilise_52,
                champ_inutilise_15 = champ_inutilise_15,
                champ_inutilise_45 = champ_inutilise_45,
                categorie_propriete = categorie_propriete,
                genre_propriete = genre_propriete,
                type_batiment = type_batiment,
                type_copropriete = type_copropriete,
                niveau = niveau,
                nb_etages = nb_etages,
                annee_contruction = annee_contruction,
                code_annee_construction = code_annee_construction,
                champ_inutilise_16 = champ_inutilise_16,
                facade_batiment = facade_batiment,
                profondeur_batiment = profondeur_batiment,
                ind_irregulier_batiment = ind_irregulier_batiment,
                um_dimension_batiment = um_dimension_batiment,
                superficie_batiment = superficie_batiment,
                um_superficie_batiment = um_superficie_batiment,
                superficie_habitable = superficie_habitable,
                um_superficie_habitable = um_superficie_habitable,
                champ_inutilise_17 = champ_inutilise_17,
                facade_terrain = facade_terrain,
                profondeur_terrain = profondeur_terrain,
                ind_irregulier_terrain = ind_irregulier_terrain,
                um_dimension_terrain = um_dimension_terrain,
                superficie_terrain = superficie_terrain,
                um_superficie_terrain = um_superficie_terrain,
                champ_inutilise_46 = champ_inutilise_46,
                annee_evaluation = annee_evaluation,
                evaluation_municipale_terrain = evaluation_municipale_terrain,
                evaluation_municipale_batiment = evaluation_municipale_batiment,
                nb_pieces = nb_pieces,
                nb_chambres = nb_chambres,
                nb_chambres_sous_sol = nb_chambres_sous_sol,
                nb_chambres_hors_sol = nb_chambres_hors_sol,
                nb_salles_bains = nb_salles_bains,
                nb_salles_eau = nb_salles_eau,
                champ_inutilise_47 = champ_inutilise_47,
                champ_inutilise_48 = champ_inutilise_48,
                champ_inutilise_18 = champ_inutilise_18,
                champ_inutilise_19 = champ_inutilise_19,
                champ_inutilise_20 = champ_inutilise_20,
                champ_inutilise_21 = champ_inutilise_21,
                depenses_tot_exploitation = depenses_tot_exploitation,
                champ_inutilise_22 = champ_inutilise_22,
                champ_inutilise_23 = champ_inutilise_23,
                nom_plan_eau = nom_plan_eau,
                champ_inutilise_24 = champ_inutilise_24,
                champ_inutilise_25 = champ_inutilise_25,
                nb_chauffe_eau_loue = nb_chauffe_eau_loue,
                inclus_francais = inclus_francais,
                inclus_anglais = inclus_anglais,
                exclus_francais = exclus_francais,
                exclus_anglais = exclus_anglais,
                nb_unites_total = nb_unites_total,
                champ_inutilise_26 = champ_inutilise_26,
                champ_inutilise_27 = champ_inutilise_27,
                champ_inutilise_28 = champ_inutilise_28,
                champ_inutilise_29 = champ_inutilise_29,
                champ_inutilise_30 = champ_inutilise_30,
                champ_inutilise_31 = champ_inutilise_31,
                champ_inutilise_32 = champ_inutilise_32,
                champ_inutilise_49 = champ_inutilise_49,
                date_modif = date_modif,
                frequence_prix_location = frequence_prix_location,
                code_statut = code_statut,
                pourc_quote_part = pourc_quote_part,
                utilisation_commerciale = utilisation_commerciale,
                champ_inutilise_2 = champ_inutilise_2,
                nom_du_parc = nom_du_parc,
                champ_inutilise_50 = champ_inutilise_50,
                champ_inutilise_51 = champ_inutilise_51,
                raison_sociale = raison_sociale,
                en_oper_depuis = en_oper_depuis,
                ind_franchise = ind_franchise,
                champ_inutilise_33 = champ_inutilise_33,
                champ_inutilise_34 = champ_inutilise_34,
                champ_inutilise_35 = champ_inutilise_35,
                ind_opt_renouv_bail = ind_opt_renouv_bail,
                annee_mois_echeance_bail = annee_mois_echeance_bail,
                url_visite_virtuelle_francais = url_visite_virtuelle_francais,
                url_visite_virtuelle_anglais = url_visite_virtuelle_anglais,
                url_desc_detaillee = url_desc_detaillee,
                ind_taxes_prix_demande = ind_taxes_prix_demande,
                ind_taxes_prix_location_demande = ind_taxes_prix_location_demande,
                courtier_inscripteur_3 = courtier_inscripteur_3,
                bureau_inscripteur_3 = bureau_inscripteur_3,
                courtier_inscripteur_4 = courtier_inscripteur_4,
                bureau_inscripteur_4 = bureau_inscripteur_4,
                courtier1_type_divul_interet = courtier1_type_divul_interet,
                courtier2_type_divul_interet = courtier2_type_divul_interet,
                courtier3_type_divul_interet = courtier3_type_divul_interet,
                courtier4_type_divul_interet = courtier4_type_divul_interet,
                ind_vente_sans_garantie_legale = ind_vente_sans_garantie_legale,
                latitude = latitude,
                longitude = longitude,
                type_superficie_habitable = type_superficie_habitable,
                rev_pot_brut_res = rev_pot_brut_res,
                rev_pot_brut_comm = rev_pot_brut_comm,
                rev_pot_brut_stat = rev_pot_brut_stat,
                rev_pot_brut_au = rev_pot_brut_au,
                date_rev_brut_pot = date_rev_brut_pot,
                particularite_construction = particularite_construction,
                au_genre_propriete_info_f = au_genre_propriete_info_f,
                au_genre_propriete_info_a = au_genre_propriete_info_a,
                prix_demande_taxe_incl = prix_demande_taxe_incl,
                ind_visites_interactive = ind_visites_interactive,
                addenda_complet_f = addenda_complet_f,
                addenda_complet_a = addenda_complet_a,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje += f"Se encontraron múltiples coincidencias para {no_inscription}, revise la base de datos"

    mensaje += f"Incriptions creadas: {total_nuevas}, Incriptions Actualizadas: {total_actualizadas}"
    return mensaje

def uploadPhotos(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    data_txt = {(row[7]) for row in data}
    existing_keys = {(photos.no_version) for photos in Photos.objects.all()}
    photos_to_delete = Photos.objects.filter(no_version__in=existing_keys).exclude(no_version__in=data_txt)
    for photos_del in photos_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            photos_del.delete()
            mensaje += f"Photos eliminada: {photos_del}\n"
        except Photos.DoesNotExist:
            mensaje += f"Error: No se encontró la Photos a eliminar: {photos_del}\n"
    for row in data:
        no_inscription = get_id_inscription(row[0])
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = int(row[1] if row[1] else None)
        nom_fichier_photo = row[2] if row[2] else None
        valor_valeurs_fixes = row[3] if row[3] else None
        code_description_photo = get_id_valeurs(valor_valeurs_fixes,'CODE_DESCRIPTION_PHOTO')
        description_francaise = row[4] if row[4] else None
        description_anglaise = row[5] if row[5] else None
        photourl = row[6] if row[6] else None
        no_version = row[7] if row[7] else None
        date_modification = row[8] if row[8] else None
        try:
            photos = Photos.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if photos.no_inscription != no_inscription:
                photos.no_inscription = no_inscription
                cambios.append('no_inscription')
            if photos.seq != seq:
                photos.seq = seq
                cambios.append('seq')
            if photos.nom_fichier_photo != nom_fichier_photo:
                photos.nom_fichier_photo = nom_fichier_photo
                cambios.append('nom_fichier_photo')
            if photos.code_description_photo != code_description_photo:
                photos.code_description_photo = code_description_photo
                cambios.append('code_description_photo')
            if photos.description_francaise != description_francaise:
                photos.description_francaise = description_francaise
                cambios.append('description_francaise')
            if photos.description_anglaise != description_anglaise:
                photos.description_anglaise = description_anglaise
                cambios.append('description_anglaise')
            if photos.photourl != photourl:
                photos.photourl = photourl
                cambios.append('photourl')
            if photos.no_version != no_version:
                photos.no_version = no_version
                cambios.append('no_version')
            if photos.date_modification != date_modification:
                photos.date_modification = date_modification
                cambios.append('date_modification')
            if cambios:
                photos.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            photos = Photos.objects.create(
                no_inscription = no_inscription,
                seq = seq,
                nom_fichier_photo = nom_fichier_photo,
                code_description_photo = code_description_photo,
                description_francaise = description_francaise,
                description_anglaise = description_anglaise,
                photourl = photourl,
                no_version = no_version,
                date_modification = date_modification,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_inscription}-{seq}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Photos cuya Incriptions no existen. "
    mensaje += f"Photos creadas: {total_nuevas}, Photos Actualizadas: {total_actualizadas}, Photos Eliminadas: {total_eliminadas}"
    return mensaje

def uploadLiensAdditionnels(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(liens.no_inscription.no_inscription, liens.seq) for liens in LiensAdditionnels.objects.all()}
    liens_to_delete = existing_keys.difference(data_txt)

    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    for liens_del in liens_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription_value, seq = liens_del
            LiensAdditionnels.objects.filter(no_inscription__no_inscription=no_inscription_value, seq=seq).delete()
            mensaje += f"LiensAdditionnels eliminada: {liens_del}\n"
        except LiensAdditionnels.DoesNotExist:
            mensaje += f"Error: No se encontró la LiensAdditionnels a eliminar: {liens_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = int(row[1] if row[1] else None)
        valor_valeurs_fixes = row[2]
        type_lien = get_id_valeurs(valor_valeurs_fixes,'TYPE_LIEN')
        lien_francais = row[3] if row[3] else None
        lien_anglais = row[4] if row[4] else None
        try:
            liensA = LiensAdditionnels.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if liensA.type_lien != type_lien:
                liensA.type_lien = type_lien
                cambios.append('type_lien')
            if liensA.lien_francais != lien_francais:
                liensA.lien_francais = lien_francais
                cambios.append('lien_francais')
            if liensA.lien_anglais != lien_anglais:
                liensA.lien_anglais = lien_anglais
                cambios.append('lien_anglais')
            if cambios:
                liensA.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            liensAdditionnels = LiensAdditionnels.objects.create(
                no_inscription = no_inscription,
                seq = seq,
                type_lien = type_lien,
                lien_francais = lien_francais,
                lien_anglais = lien_anglais,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_inscription}-{seq}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene LiensAdditionnels cuya Incriptions no existen. "
    mensaje += f"LiensAdditionnels creadas: {total_nuevas}, LiensAdditionnels Actualizadas: {total_actualizadas}, LiensAdditionnels Eliminadas: {total_eliminadas}"
    return mensaje

def uploadVisitesLibres(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0

    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(visites.no_inscription.no_inscription, visites.seq) for visites in VisitesLibres.objects.all()}
    visites_to_delete = existing_keys.difference(data_txt)

    for visites_del in visites_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription_value, seq = visites_del
            VisitesLibres.objects.filter(no_inscription__no_inscription=no_inscription_value, seq=seq).delete()
            mensaje += f"VisitesLibres eliminada: {visites_del}\n"
        except VisitesLibres.DoesNotExist:
            mensaje += f"Error: No se encontró la VisitesLibres a eliminar: {visites_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = int(row[1] if row[1] else None)
        date_debut = row[2] if row[2] else None
        date_fin = row[3] if row[3] else None
        heure_debut = row[4] if row[4] else None
        heure_fin = row[5] if row[5] else None
        commentaires_f = row[6] if row[6] else None
        commentaires_a = row[7] if row[7] else None
        valor_valeurs_fixes = row[8]
        code_visite_caravane = get_id_valeurs(valor_valeurs_fixes,'CODE_VISITE_CARAVANE')
        lien_visite_virt = row[9] if row[9] else None
        try:
            visites = VisitesLibres.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if visites.date_debut != date_debut:
                visites.date_debut = date_debut
                cambios.append('date_debut')
            if visites.date_fin != date_fin:
                visites.date_fin = date_fin
                cambios.append('date_fin')
            if visites.heure_debut != heure_debut:
                visites.heure_debut = heure_debut
                cambios.append('heure_debut')
            if visites.heure_fin != heure_fin:
                visites.heure_fin = heure_fin
                cambios.append('heure_fin')
            if visites.commentaires_f != commentaires_f:
                visites.commentaires_f = commentaires_f
                cambios.append('commentaires_f')
            if visites.commentaires_a != commentaires_a:
                visites.commentaires_a = commentaires_a
                cambios.append('commentaires_a')
            if visites.code_visite_caravane != code_visite_caravane:
                visites.code_visite_caravane = code_visite_caravane
                cambios.append('code_visite_caravane')
            if visites.lien_visite_virt != lien_visite_virt:
                visites.lien_visite_virt = lien_visite_virt
                cambios.append('lien_visite_virt')
            if cambios:
                visites.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            visitesLibres = VisitesLibres.objects.create(
                no_inscription = no_inscription,
                seq = seq,
                date_debut = date_debut,
                date_fin = date_fin,
                heure_debut = heure_debut,
                heure_fin = heure_fin,
                commentaires_f = commentaires_f,
                commentaires_a = commentaires_a,
                code_visite_caravane = code_visite_caravane,
                lien_visite_virt = lien_visite_virt,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_inscription}-{seq}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene VisitesLibres cuya Incriptions no existen. "
    mensaje += f"VisitesLibres creadas: {total_nuevas}, VisitesLibres Actualizadas: {total_actualizadas}, VisitesLibres Eliminadas: {total_eliminadas}"
    return mensaje

def uploadRemarques(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(remarques.no_inscription.no_inscription, remarques.no_remarque) for remarques in Remarques.objects.all()}
    remarques_to_delete = existing_keys.difference(data_txt)

    for remarques_del in remarques_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription_value, no_remarque = remarques_del
            Remarques.objects.filter(no_inscription__no_inscription=no_inscription_value, no_remarque=no_remarque).delete()
            mensaje += f"Remarques eliminada: {remarques_del}\n"
        except Remarques.DoesNotExist:
            mensaje += f"Error: No se encontró la Remarques a eliminar: {remarques_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        no_remarque = int(row[1] if row[1] else None)
        valor_valeurs_fixes = row[2] if row[2] else None
        code_langue = get_id_valeurs(valor_valeurs_fixes,'CODE_LANGUE')
        ordre_affichage = int(row[3] if row[3] else None)
        champ_inutilise_1 = row[4] if row[4] else None
        champ_inutilise_2 = row[5] if row[5] else None
        texte = row[6] if row[6] else None
        try:
            remarques = Remarques.objects.get(no_inscription=no_inscription, no_remarque=no_remarque)
            cambios = []
            if remarques.code_langue != code_langue:
                remarques.code_langue = code_langue
                cambios.append('code_langue')
            if remarques.ordre_affichage != ordre_affichage:
                remarques.ordre_affichage = ordre_affichage
                cambios.append('ordre_affichage')
            if remarques.champ_inutilise_1 != champ_inutilise_1:
                remarques.champ_inutilise_1 = champ_inutilise_1
                cambios.append('champ_inutilise_1')
            if remarques.champ_inutilise_2 != champ_inutilise_2:
                remarques.champ_inutilise_2 = champ_inutilise_2
                cambios.append('champ_inutilise_2')
            if remarques.texte != texte:
                remarques.texte = texte
                cambios.append('texte')
            if cambios:
                remarques.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            remarques = Remarques.objects.create(
                no_inscription = no_inscription,
                no_remarque = no_remarque,
                code_langue = code_langue,
                ordre_affichage = ordre_affichage,
                champ_inutilise_1 = champ_inutilise_1,
                champ_inutilise_2 = champ_inutilise_2,
                texte = texte,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_inscription}-{no_remarque}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Remarques cuya Incriptions no existen. "
    mensaje += f"Remarques creadas: {total_nuevas}, Remarques Actualizadas: {total_actualizadas}, Remarques Eliminadas: {total_eliminadas}"
    return mensaje

def uploadUnitesDetaillees(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(detaillees.no_inscription.no_inscription, detaillees.seq) for detaillees in UnitesDetaillees.objects.all()}
    detaillees_to_delete = existing_keys.difference(data_txt)

    for detaillees_del in detaillees_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription_value, seq = detaillees_del
            UnitesDetaillees.objects.filter(no_inscription__no_inscription=no_inscription_value, seq=seq).delete()
            mensaje += f"UnitesDetaillees eliminada: {detaillees_del}\n"
        except UnitesDetaillees.DoesNotExist:
            mensaje += f"Error: No se encontró la UnitesDetaillees a eliminar: {detaillees_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = int(row[1]) if row[1] else None
        valor_valeurs_fixes = row[2]
        type_unite_det = get_id_valeurs(valor_valeurs_fixes,'TYPE_UNITE_DET')
        nb_pieces = int(row[3]) if row[3] else None
        nb_chambres = int(row[4]) if row[4] else None
        inclus_chauffage = row[5] if row[5] else None
        inclus_electricite = row[6] if row[6] else None
        inclus_eau_chaude = row[7] if row[7] else None
        inclus_taxe_eau = row[8] if row[8] else None
        inclus_pelouse = row[9] if row[9] else None
        inclus_deneigement = row[10] if row[10] else None
        inclus_meuble = row[11] if row[11] else None
        inclus_semi_meuble = row[12] if row[12] else None
        nb_stat_interieurs = row[13] if row[13] else None
        nb_stat_exterieurs = row[14] if row[14] else None
        au_inclus_info_f = row[15] if row[15] else None
        au_inclus_info_a = row[16] if row[16] else None
        ind_vacant = row[17] if row[17] else None
        superficie_totale = row[18] if row[18] else None
        valor_valeurs_fixes = row[19]
        um_superficie_totale = get_id_valeurs(valor_valeurs_fixes,'UM_SUPERFICIE_TOTALE')
        try:
            detaillees = UnitesDetaillees.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if detaillees.type_unite_det != type_unite_det:
                detaillees.type_unite_det = type_unite_det
                cambios.append('type_unite_det')
            if detaillees.nb_pieces != nb_pieces:
                detaillees.nb_pieces = nb_pieces
                cambios.append('nb_pieces')
            if detaillees.nb_chambres != nb_chambres:
                detaillees.nb_chambres = nb_chambres
                cambios.append('nb_chambres')
            if detaillees.inclus_chauffage != inclus_chauffage:
                detaillees.inclus_chauffage = inclus_chauffage
                cambios.append('inclus_chauffage')
            if detaillees.inclus_electricite != inclus_electricite:
                detaillees.inclus_electricite = inclus_electricite
                cambios.append('inclus_electricite')
            if detaillees.inclus_eau_chaude != inclus_eau_chaude:
                detaillees.inclus_eau_chaude = inclus_eau_chaude
                cambios.append('inclus_eau_chaude')
            if detaillees.inclus_taxe_eau != inclus_taxe_eau:
                detaillees.inclus_taxe_eau = inclus_taxe_eau
                cambios.append('inclus_taxe_eau')
            if detaillees.inclus_pelouse != inclus_pelouse:
                detaillees.inclus_pelouse = inclus_pelouse
                cambios.append('inclus_pelouse')
            if detaillees.inclus_deneigement != inclus_deneigement:
                detaillees.inclus_deneigement = inclus_deneigement
                cambios.append('inclus_deneigement')
            if detaillees.inclus_meuble != inclus_meuble:
                detaillees.inclus_meuble = inclus_meuble
                cambios.append('inclus_meuble')
            if detaillees.inclus_semi_meuble != inclus_semi_meuble:
                detaillees.inclus_semi_meuble = inclus_semi_meuble
                cambios.append('inclus_semi_meuble')
            if detaillees.nb_stat_interieurs != nb_stat_interieurs:
                detaillees.nb_stat_interieurs = nb_stat_interieurs
                cambios.append('nb_stat_interieurs')
            if detaillees.nb_stat_exterieurs != nb_stat_exterieurs:
                detaillees.nb_stat_exterieurs = nb_stat_exterieurs
                cambios.append('nb_stat_exterieurs')
            if detaillees.au_inclus_info_f != au_inclus_info_f:
                detaillees.au_inclus_info_f = au_inclus_info_f
                cambios.append('au_inclus_info_f')
            if detaillees.au_inclus_info_a != au_inclus_info_a:
                detaillees.au_inclus_info_a = au_inclus_info_a
                cambios.append('au_inclus_info_a')
            if detaillees.ind_vacant != ind_vacant:
                detaillees.ind_vacant = ind_vacant
                cambios.append('ind_vacant')
            if detaillees.superficie_totale != superficie_totale:
                detaillees.superficie_totale = superficie_totale
                cambios.append('superficie_totale')
            if detaillees.um_superficie_totale != um_superficie_totale:
                detaillees.um_superficie_totale = um_superficie_totale
                cambios.append('um_superficie_totale')
            if cambios:
                detaillees.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            detaillees = UnitesDetaillees.objects.create(
            no_inscription = no_inscription,
            seq = seq,
            type_unite_det = type_unite_det,
            nb_pieces = nb_pieces,
            nb_chambres = nb_chambres,
            inclus_chauffage = inclus_chauffage,
            inclus_electricite = inclus_electricite,
            inclus_eau_chaude = inclus_eau_chaude,
            inclus_taxe_eau = inclus_taxe_eau,
            inclus_pelouse = inclus_pelouse,
            inclus_deneigement = inclus_deneigement,
            inclus_meuble = inclus_meuble,
            inclus_semi_meuble = inclus_semi_meuble,
            nb_stat_interieurs = nb_stat_interieurs,
            nb_stat_exterieurs = nb_stat_exterieurs,
            au_inclus_info_f = au_inclus_info_f,
            au_inclus_info_a = au_inclus_info_a,
            ind_vacant = ind_vacant,
            superficie_totale = superficie_totale,
            um_superficie_totale = um_superficie_totale,
        )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_inscription}-{seq}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene UnitesDetaillees cuya Incriptions no existen. "
    mensaje += f"UnitesDetaillees creadas: {total_nuevas}, UnitesDetaillees Actualizadas: {total_actualizadas}, UnitesDetaillees Eliminadas: {total_eliminadas}"
    return mensaje

def uploadAddenda(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    data_txt = {(str(row[0]),int(row[1]),str(row[2]),int(row[3])) for row in data}
    existing_keys = {(addenda.no_inscription.no_inscription, addenda.no_addenda, addenda.code_langue.valeur, addenda.ordre_affichage) for addenda in Addenda.objects.all()}
    addenda_to_delete = existing_keys.difference(data_txt)
    for addenda_del in addenda_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, no_addenda, code_langue, ordre_affichage = addenda_del
            Addenda.objects.filter(
                no_inscription__no_inscription=no_inscription,
                no_addenda=no_addenda,
                code_langue=code_langue,
                ordre_affichage=ordre_affichage
            ).delete()
            mensaje += f"UnitesDetaillees eliminada: {addenda_del}\n"
        except Addenda.DoesNotExist:
            mensaje += f"Error: No se encontró la UnitesDetaillees a eliminar: {addenda_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        no_addenda = int(row[1]) if row[1] else None
        valor_valeurs_fixes = row[2]
        code_langue = get_id_valeurs(valor_valeurs_fixes,'CODE_LANGUE')
        ordre_affichage = int(row[3]) if row[3] else None
        champ_inutilise_1 = row[4] if row[4] else None
        champ_inutilise_2 = row[5] if row[5] else None
        texte = row[6] if row[6] else None
        try:
            addenda = Addenda.objects.get(
                no_inscription=no_inscription,
                no_addenda=no_addenda,
                code_langue=code_langue,
                ordre_affichage=ordre_affichage,
            )
            cambios = []
            if addenda.champ_inutilise_1 != champ_inutilise_1:
                addenda.champ_inutilise_1 = champ_inutilise_1
                cambios.append('champ_inutilise_1')
            if addenda.champ_inutilise_2 != champ_inutilise_2:
                addenda.champ_inutilise_2 = champ_inutilise_2
                cambios.append('champ_inutilise_2')
            if addenda.texte != texte:
                addenda.texte = texte
                cambios.append('texte')
            if cambios:
                addenda.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            addenda = Addenda.objects.create(
                no_inscription = no_inscription,
                no_addenda = no_addenda,
                code_langue = code_langue,
                ordre_affichage = ordre_affichage,
                champ_inutilise_1 = champ_inutilise_1,
                champ_inutilise_2 = champ_inutilise_2,
                texte = texte,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {no_addenda}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Addendas cuya Incriptions no existen. "
    mensaje += f"Addendas creadas: {total_nuevas}, Addendas Actualizadas: {total_actualizadas}, Addendas Eliminadas: {total_eliminadas}"
    return mensaje

def uploadUnitesSommaires(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(sommaires.no_inscription.no_inscription, sommaires.seq) for sommaires in UnitesSommaires.objects.all()}
    sommaires_to_delete = existing_keys.difference(data_txt)
    for sommaires_del in sommaires_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, seq = sommaires_del
            UnitesSommaires.objects.filter(
                no_inscription__no_inscription=no_inscription,
                seq=seq,
            ).delete()
            mensaje += f"UnitesSommaires eliminada: {sommaires_del}\n"
        except UnitesSommaires.DoesNotExist:
            mensaje += f"Error: No se encontró la UnitesSommaires a eliminar: {sommaires_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = int(row[1]) if row[1] else None 
        valor_valeurs_fixes = row[2]
        type_unite_som = get_id_valeurs(valor_valeurs_fixes,'TYPE_UNITE_SOM')
        nb_total_unites = int(row[3]) if row[3] else None 
        nb_unites_vacantes = int(row[4]) if row[4] else None 
        au_unite_revenu_info_f = row[5] if row[5] else None 
        au_unite_revenu_info_a = row[6] if row[6] else None 
        try:
            sommaires = UnitesSommaires.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if sommaires.no_inscription != no_inscription:
                sommaires.no_inscription = no_inscription
                cambios.append('no_inscription')
            if sommaires.seq != seq:
                sommaires.seq = seq
                cambios.append('seq')
            if sommaires.type_unite_som != type_unite_som:
                sommaires.type_unite_som = type_unite_som
                cambios.append('type_unite_som')
            if sommaires.nb_total_unites != nb_total_unites:
                sommaires.nb_total_unites = nb_total_unites
                cambios.append('nb_total_unites')
            if sommaires.nb_unites_vacantes != nb_unites_vacantes:
                sommaires.nb_unites_vacantes = nb_unites_vacantes
                cambios.append('nb_unites_vacantes')
            if sommaires.au_unite_revenu_info_f != au_unite_revenu_info_f:
                sommaires.au_unite_revenu_info_f = au_unite_revenu_info_f
                cambios.append('au_unite_revenu_info_f')
            if sommaires.au_unite_revenu_info_a != au_unite_revenu_info_a:
                sommaires.au_unite_revenu_info_a = au_unite_revenu_info_a
                cambios.append('au_unite_revenu_info_a')
            if cambios:
                sommaires.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            sommaires = UnitesSommaires.objects.create(
                no_inscription = no_inscription,
                seq = seq,
                type_unite_som = type_unite_som,
                nb_total_unites = nb_total_unites,
                nb_unites_vacantes = nb_unites_vacantes,
                au_unite_revenu_info_f = au_unite_revenu_info_f,
                au_unite_revenu_info_a = au_unite_revenu_info_a,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {sommaires}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene UnitesSommaires cuya Incriptions no existen. "
    mensaje += f"UnitesSommaires creadas: {total_nuevas}, UnitesSommaires Actualizadas: {total_actualizadas}, UnitesSommaires Eliminadas: {total_eliminadas}"
    return mensaje

def uploadDepenses(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    data_txt = {(str(row[0]),row[1]) for row in data}
    existing_keys = {(depenses.no_inscription.no_inscription, depenses.tdep_code.valeur) for depenses in Depenses.objects.all()}
    
    depenses_to_delete = existing_keys.difference(data_txt)
    for depenses_del in depenses_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, tdep_code = depenses_del
            Depenses.objects.filter(
                no_inscription__no_inscription=no_inscription,
                tdep_code__valeur=tdep_code,
            ).delete()
            mensaje += f"Depenses eliminada: {depenses_del}\n"
        except Depenses.DoesNotExist:
            mensaje += f"Error: No se encontró la Depenses a eliminar: {depenses_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        valor_valeurs_fixes = row[1]
        tdep_code = get_id_valeurs(valor_valeurs_fixes,'TYPE_DEPENSE')
        montant_depense = int(row[2]) if row[2] else None
        annee = int(row[3]) if row[3] else None
        annee_expiration = int(row[4]) if row[4] else None
        valor_valeurs_fixes = row[5]
        frequence = get_id_valeurs(valor_valeurs_fixes,'FREQUENCE_DEPENSE')
        valor_valeurs_fixes = row[6]
        part_depense = get_id_valeurs(valor_valeurs_fixes,'PART_DEPENSE')
        au_depense_info_f = row[7] if row[7] else None
        au_depense_info_a = row[8] if row[8] else None
        try:
            depenses = Depenses.objects.get(no_inscription=no_inscription, tdep_code=tdep_code)
            cambios = []
            if depenses.montant_depense != montant_depense:
                depenses.montant_depense = montant_depense
                cambios.append('montant_depense')
            if depenses.annee != annee:
                depenses.annee = annee
                cambios.append('annee')
            if depenses.annee_expiration != annee_expiration:
                depenses.annee_expiration = annee_expiration
                cambios.append('annee_expiration')
            if depenses.frequence != frequence:
                depenses.frequence = frequence
                cambios.append('frequence')
            if depenses.part_depense != part_depense:
                depenses.part_depense = part_depense
                cambios.append('part_depense')
            if depenses.au_depense_info_f != au_depense_info_f:
                depenses.au_depense_info_f = au_depense_info_f
                cambios.append('au_depense_info_f')
            if depenses.au_depense_info_a != au_depense_info_a:
                depenses.au_depense_info_a = au_depense_info_a
                cambios.append('au_depense_info_a')
            if cambios:
                depenses.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            
            depenses = Depenses.objects.create(
                no_inscription = no_inscription,
                tdep_code = tdep_code,
                montant_depense = montant_depense,
                annee = annee,
                annee_expiration = annee_expiration,
                frequence = frequence,
                part_depense = part_depense,
                au_depense_info_f = au_depense_info_f,
                au_depense_info_a = au_depense_info_a,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {depenses}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Depenses cuya Incriptions no existen. "
    mensaje += f"Depenses creadas: {total_nuevas}, Depenses Actualizadas: {total_actualizadas}, Depenses Eliminadas: {total_eliminadas}"
    return mensaje

def uploadRenovations(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    data_txt = {(str(row[0]),int(row[1])) for row in data}
    existing_keys = {(renovations.no_inscription.no_inscription, renovations.seq) for renovations in Renovations.objects.all()}
    renovations_to_delete = existing_keys.difference(data_txt)
    for renovations_del in renovations_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, seq = renovations_del
            Renovations.objects.filter(
                no_inscription__no_inscription=no_inscription,
                seq=seq,
            ).delete()
            mensaje += f"Renovations eliminada: {renovations_del}\n"
        except Renovations.DoesNotExist:
            mensaje += f"Error: No se encontró la Renovations a eliminar: {renovations_del}\n"
    for row in data:
        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq = row[1]
        valor_valeurs_fixes = row[2]
        renovation_type = get_id_valeurs(valor_valeurs_fixes,'RENOVATION_TYPE')
        annee = int(row[3]) if row[3] else None
        champ_inutilise_1 = int(row[4]) if row[4] else None
        informations_francaises = row[5]
        informations_anglaises = row[6]
        montant = int(row[7]) if row[7] else None
        try:
            renovations = Renovations.objects.get(no_inscription=no_inscription, seq=seq)
            cambios = []
            if renovations.renovation_type != renovation_type:
                renovations.renovation_type = renovation_type
                cambios.append('renovation_type')
            if renovations.annee != annee:
                renovations.annee = annee
                cambios.append('annee')
            if renovations.champ_inutilise_1 != champ_inutilise_1:
                renovations.champ_inutilise_1 = champ_inutilise_1
                cambios.append('champ_inutilise_1')
            if renovations.informations_francaises != informations_francaises:
                renovations.informations_francaises = informations_francaises
                cambios.append('informations_francaises')
            if renovations.informations_anglaises != informations_anglaises:
                renovations.informations_anglaises = informations_anglaises
                cambios.append('informations_anglaises')
            if renovations.montant != montant:
                renovations.montant = montant
                cambios.append('montant')
            if cambios:
                renovations.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            renovations = Renovations.objects.create(
                no_inscription = no_inscription,
                seq = seq,
                renovation_type = renovation_type,
                annee = annee,
                champ_inutilise_1 = champ_inutilise_1,
                informations_francaises = informations_francaises,
                informations_anglaises = informations_anglaises,
                montant = montant,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {renovations}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Renovations cuya Incriptions no existen. "
    mensaje += f"Renovations creadas: {total_nuevas}, Renovations Actualizadas: {total_actualizadas}, Renovations Eliminadas: {total_eliminadas}"
    return mensaje

def uploadPiecesUnites(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    data_txt = {(str(row[0]),int(row[1]),int(row[2])) for row in data}
    existing_keys = {(pieces.no_inscription.no_inscription, pieces.seq_unite_det, pieces.seq) for pieces in PiecesUnites.objects.all()}
    pieces_to_delete = existing_keys.difference(data_txt)
    for pieces_del in pieces_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, seq_unite_det, seq = pieces_del
            PiecesUnites.objects.filter(
                no_inscription__no_inscription=no_inscription,
                seq_unite_det=seq_unite_det,
                seq=seq,
            ).delete()
            mensaje += f"PiecesUnites eliminada: {pieces_del}\n"
        except PiecesUnites.DoesNotExist:
            mensaje += f"Error: No se encontró la PiecesUnites a eliminar: {pieces_del}\n"
    for row in data:
        no_inscription = get_id_inscription(row[0])
        if no_inscription == None:
            errors.append(row[0])
            continue
        seq_unite_det = int(row[1]) if row[1] else None 
        seq = int(row[2]) if row[2] else None 
        valor_valeurs_fixes = row[3]
        piece_code = get_id_valeurs(valor_valeurs_fixes,'PIECE_CODE')
        au_piece_info_f = row[4] if row[4] else None
        au_piece_info_a = row[5] if row[5] else None
        valor_valeurs_fixes = row[6]
        niveau = get_id_valeurs(valor_valeurs_fixes,'NIVEAU')
        au_niveau_info_f = row[7] if row[7] else None
        au_niveau_info_a = row[8] if row[8] else None
        dimensions = row[9] if row[9] else None
        ind_irregulier = row[10] if row[10] else None
        valor_valeurs_fixes = row[11]
        couvre_plancher_code = get_id_valeurs(valor_valeurs_fixes,'COUVRE_PLANCHER_CODE')
        au_couvre_plancher_f = row[12] if row[12] else None
        au_couvre_plancher_a = row[13] if row[13] else None
        ind_foyer_poele = row[14] if row[14] else None
        info_supp_f = row[15] if row[15] else None
        info_supp_a = row[16] if row[16] else None
        try:
            pieces = PiecesUnites.objects.get(no_inscription=no_inscription, seq_unite_det=seq_unite_det, seq=seq)
            cambios = []
            if pieces.au_piece_info_f != au_piece_info_f:
                pieces.au_piece_info_f = au_piece_info_f
                cambios.append('au_piece_info_f')
            if pieces.au_piece_info_a != au_piece_info_a:
                pieces.au_piece_info_a = au_piece_info_a
                cambios.append('au_piece_info_a')
            if pieces.niveau != niveau:
                pieces.niveau = niveau
                cambios.append('niveau')
            if pieces.au_niveau_info_f != au_niveau_info_f:
                pieces.au_niveau_info_f = au_niveau_info_f
                cambios.append('au_niveau_info_f')
            if pieces.au_niveau_info_a != au_niveau_info_a:
                pieces.au_niveau_info_a = au_niveau_info_a
                cambios.append('au_niveau_info_a')
            if pieces.dimensions != dimensions:
                pieces.dimensions = dimensions
                cambios.append('dimensions')
            if pieces.ind_irregulier != ind_irregulier:
                pieces.ind_irregulier = ind_irregulier
                cambios.append('ind_irregulier')
            if pieces.couvre_plancher_code != couvre_plancher_code:
                pieces.couvre_plancher_code = couvre_plancher_code
                cambios.append('couvre_plancher_code')
            if pieces.au_couvre_plancher_f != au_couvre_plancher_f:
                pieces.au_couvre_plancher_f = au_couvre_plancher_f
                cambios.append('au_couvre_plancher_f')
            if pieces.au_couvre_plancher_a != au_couvre_plancher_a:
                pieces.au_couvre_plancher_a = au_couvre_plancher_a
                cambios.append('au_couvre_plancher_a')
            if pieces.ind_foyer_poele != ind_foyer_poele:
                pieces.ind_foyer_poele = ind_foyer_poele
                cambios.append('ind_foyer_poele')
            if pieces.info_supp_f != info_supp_f:
                pieces.info_supp_f = info_supp_f
                cambios.append('info_supp_f')
            if pieces.info_supp_a != info_supp_a:
                pieces.info_supp_a = info_supp_a
                cambios.append('info_supp_a')
            if cambios:
                pieces.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            pieces = PiecesUnites.objects.create(
                no_inscription = no_inscription,
                seq_unite_det = seq_unite_det,
                seq = seq,
                piece_code = piece_code,
                au_piece_info_f = au_piece_info_f,
                au_piece_info_a = au_piece_info_a,
                niveau = niveau,
                au_niveau_info_f = au_niveau_info_f,
                au_niveau_info_a = au_niveau_info_a,
                dimensions = dimensions,
                ind_irregulier = ind_irregulier,
                couvre_plancher_code = couvre_plancher_code,
                au_couvre_plancher_f = au_couvre_plancher_f,
                au_couvre_plancher_a = au_couvre_plancher_a,
                ind_foyer_poele = ind_foyer_poele,
                info_supp_f = info_supp_f,
                info_supp_a = info_supp_a,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {pieces}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene PiecesUnites cuya Incriptions no existen. "
    mensaje += f"PiecesUnites creadas: {total_nuevas}, PiecesUnites Actualizadas: {total_actualizadas}, PiecesUnites Eliminadas: {total_eliminadas}"
    return mensaje


def uploadCaracteristiques(data):
    mensaje = ''
    total_actualizadas = 0
    total_nuevas = 0
    errors = []
    total_eliminadas = 0
    if not data:
        return "El archivo está en blanco. No hay datos para procesar."
    data_txt = {(str(row[0]),str(row[1]),str(row[2])) for row in data}
    existing_keys = {(caracteristiques.no_inscription.no_inscription, caracteristiques.tcar_code.code, caracteristiques.scarac_code.code) for caracteristiques in Caracteristiques.objects.all()}
    caracteristiques_to_delete = existing_keys.difference(data_txt)
    for caracteristiques_del in caracteristiques_to_delete:
        total_eliminadas = total_eliminadas + 1
        try:
            no_inscription, tcar_code, scarac_code = caracteristiques_del
            Caracteristiques.objects.filter(
                no_inscription__no_inscription=no_inscription,
                tcar_code__code=tcar_code,
                scarac_code__code=scarac_code,
            ).delete()
            mensaje += f"Caracteristiques eliminada: {caracteristiques_del}\n"
        except Caracteristiques.DoesNotExist:
            mensaje += f"Error: No se encontró la Caracteristiques a eliminar: {caracteristiques_del}\n"
    for row in data:
        # pdb.set_trace()

        no_inscription = get_id_inscription(str(row[0]))
        if no_inscription == None:
            errors.append(row[0])
            continue
        tcar_code = get_id_tcar_code(str(row[1]))
        # print(tcar_code)
        scarac_code = get_id_scarac_code(str(row[2]),tcar_code)
        # print(scarac_code)
        nombre = int(row[3]) if row[3] else None
        informations_francaises = row[4] if row[4] else None
        informations_anglaises = row[5] if row[5] else None
        montant = int(row[6]) if row[6] else None
        try:
            caracteristiques = Caracteristiques.objects.get(no_inscription=no_inscription, tcar_code=tcar_code, scarac_code=scarac_code)
            cambios = []
            if caracteristiques.nombre != nombre:
                caracteristiques.nombre = nombre
                cambios.append('nombre')
            if caracteristiques.informations_francaises != informations_francaises:
                caracteristiques.informations_francaises = informations_francaises
                cambios.append('informations_francaises')
            if caracteristiques.informations_anglaises != informations_anglaises:
                caracteristiques.informations_anglaises = informations_anglaises
                cambios.append('informations_anglaises')
            if caracteristiques.montant != montant:
                caracteristiques.montant = montant
                cambios.append('montant')
            if cambios:
                caracteristiques.save()
                total_actualizadas = total_actualizadas + 1
        except ObjectDoesNotExist:
            # pdb.set_trace()
            caracteristiques = Caracteristiques.objects.create(
                no_inscription = no_inscription,
                tcar_code = tcar_code,
                scarac_code = scarac_code,
                nombre = nombre,
                informations_francaises = informations_francaises,
                informations_anglaises = informations_anglaises,
                montant = montant,
            )
            total_nuevas = total_nuevas + 1
        except MultipleObjectsReturned:
            mensaje = f"Se encontraron múltiples coincidencias para {row}, revise la base de datos"
    if errors:
        mensaje="El archivo TXT contiene Caracteristiques cuya Incriptions no existen. "
    mensaje += f"Caracteristiques creadas: {total_nuevas}, Depenses Actualizadas: {total_actualizadas}, Caracteristiques Eliminadas: {total_eliminadas}"
    return mensaje








def get_id_valeurs(valor, domaine):
    try:
        valeur = ValeursFixes.objects.get(domaine=domaine, valeur=valor)
        return valeur
    except ValeursFixes.DoesNotExist:
        return None

def get_id_municipalite(code):
    try:
        municipalite = Municipalites.objects.get(code=code)
        return municipalite
    except Municipalites.DoesNotExist:
        return None

def get_id_bureau(code):
    try:
        bureau = Bureaux.objects.get(code=code)
        return bureau
    except Bureaux.DoesNotExist:
        return None

def get_id_courtier(code):
    try:
        membre = Membres.objects.get(code=code)
        return membre
    except Membres.DoesNotExist:
        return None

def get_id_quartiers(code, municipalite):
    try:
        quartier = Quartiers.objects.get(code=code, mun_code=municipalite)
        return quartier
    except Quartiers.DoesNotExist:
        return None

def get_id_genres_proprietes(code):
    try:
        quartier = GenresProprietes.objects.get(genre_propriete=code)
        return quartier
    except GenresProprietes.DoesNotExist:
        return None
    
def get_id_inscription(code):
    try:
        inscription = Inscriptions.objects.get(no_inscription=code)
        return inscription
    except Inscriptions.DoesNotExist:
        return None 

def get_id_tcar_code(code):
    try:
        tcar_code = TypeCaracteristiques.objects.get(code=code)
        return tcar_code
    except TypeCaracteristiques.DoesNotExist:
        return None

def get_id_scarac_code(code, tcar_code):
    try:
        scarac_code = SousTypeCaracteristiques.objects.get(code=code, tcar_code=tcar_code)
        return scarac_code
    except SousTypeCaracteristiques.DoesNotExist:
        return None
