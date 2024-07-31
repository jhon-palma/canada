from django.db import models
import uuid

class Propertie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug_en = models.SlugField(max_length=500, blank=True)
    slug_fr = models.SlugField(max_length=500, blank=True)
    
    class Meta:
        db_table = 'properties'
        verbose_name = 'properties'
        verbose_name_plural = 'Create Propertie'
        ordering = ['id']

class ValeursFixes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    domaine = models.CharField(db_column='DOMAINE', max_length=70, blank=True, null=True)  
    valeur = models.CharField(db_column='VALEUR', max_length=10, blank=True, null=True)  
    description_abregee_francaise = models.CharField(db_column='DESCRIPTION_ABREGEE_FRANCAISE', max_length=15, blank=True, null=True)  
    description_abregee_anglaise = models.CharField(db_column='DESCRIPTION_ABREGEE_ANGLAISE', max_length=15, blank=True, null=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=150, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=150, blank=True, null=True)  

    class Meta:
        db_table = 'VALEURS_FIXES'

class TypesBannieres(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=10, unique=True)  
    nom_francais = models.CharField(db_column='NOM_FRANCAIS', max_length=60, blank=True, null=True)  
    nom_anglais = models.CharField(db_column='NOM_ANGLAIS', max_length=60, blank=True, null=True)  
    nom_abrege_francais = models.CharField(db_column='NOM_ABREGE_FRANCAIS', max_length=15, blank=True, null=True)  
    nom_abrege_anglais = models.CharField(db_column='NOM_ABREGE_ANGLAIS', max_length=15, blank=True, null=True)  

    class Meta:
        db_table = 'TYPES_BANNIERES'

class Regions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=2, unique=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  

    class Meta:
        db_table = 'REGIONS'
        
class Municipalites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=6, unique=True)  
    description = models.CharField(db_column='DESCRIPTION', max_length=60, blank=True, null=True)  
    region_code = models.ForeignKey(Regions, on_delete=models.CASCADE, to_field='code', db_column='REGION_CODE')   

    class Meta:
        db_table = 'MUNICIPALITES'

class Quartiers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    mun_code = models.ForeignKey(Municipalites, on_delete=models.CASCADE, to_field='code', db_column='MUN_CODE')
    code = models.CharField(db_column='CODE', max_length=4, blank=True, null=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  

    class Meta:
        db_table = 'QUARTIERS'
        unique_together = ['mun_code', 'code']

class Firmes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=12, unique=True)  
    nom_legal = models.CharField(db_column='NOM_LEGAL', max_length=80, blank=True, null=True)  
    no_certificat = models.CharField(db_column='NO_CERTIFICAT', max_length=10, blank=True, null=True)  
    type_certificat = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_CERTIFICAT_FIRME',db_column='TYPE_CERTIFICAT', blank=True, null=True)  
    banniere_code = models.ForeignKey(TypesBannieres, on_delete=models.CASCADE, to_field='code', db_column='BANNIERE_CODE')
    firme_principale = models.CharField(db_column='FIRME_PRINCIPALE', max_length=12, blank=True, null=True)  
    courtier_code = models.CharField(db_column='COURTIER_CODE', max_length=10, blank=True, null=True)  

    class Meta:
        db_table = 'FIRMES'

class Bureaux(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=12, unique=True)  
    firme_code = models.ForeignKey(Firmes, on_delete=models.CASCADE, to_field='code', db_column='FIRME_CODE')  
    nom_legal = models.CharField(db_column='NOM_LEGAL', max_length=40, blank=True, null=True)  
    no_civique = models.CharField(db_column='NO_CIVIQUE', max_length=10, blank=True, null=True)  
    nom_rue = models.CharField(db_column='NOM_RUE', max_length=60, blank=True, null=True)  
    bureau = models.CharField(db_column='BUREAU', max_length=10, blank=True, null=True)  
    municipalite = models.CharField(db_column='MUNICIPALITE', max_length=50, blank=True, null=True)  
    province = models.CharField(db_column='PROVINCE', max_length=10, blank=True, null=True)  
    code_postal = models.CharField(db_column='CODE_POSTAL', max_length=6, blank=True, null=True)  
    telephone_1 = models.CharField(db_column='TELEPHONE_1', max_length=20, blank=True, null=True)  
    poste_1 = models.CharField(db_column='POSTE_1', max_length=20, blank=True, null=True)  
    telephone_2 = models.CharField(db_column='TELEPHONE_2', max_length=20, blank=True, null=True)  
    poste_2 = models.CharField(db_column='POSTE_2', max_length=20, blank=True, null=True)  
    telephone_fax = models.CharField(db_column='TELEPHONE_FAX', max_length=20, blank=True, null=True)  
    courriel = models.CharField(db_column='COURRIEL', max_length=150, blank=True, null=True)  
    site_web = models.CharField(db_column='SITE_WEB', max_length=150, blank=True, null=True)  
    directeur_code = models.CharField(db_column='DIRECTEUR_CODE', max_length=50, blank=True, null=True)  
    url_logo_bureau = models.CharField(db_column='URL_LOGO_BUREAU', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'BUREAUX'

class GenresProprietes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    categorie_propriete = models.CharField(db_column='CATEGORIE_PROPRIETE', max_length=10, blank=True, null=True)  
    genre_propriete = models.CharField(db_column='GENRE_PROPRIETE', max_length=3, unique=True, blank=True, null=True)  
    description_abregee_francaise = models.CharField(db_column='DESCRIPTION_ABREGEE_FRANCAISE', max_length=15, blank=True, null=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_abregee_anglaise = models.CharField(db_column='DESCRIPTION_ABREGEE_ANGLAISE', max_length=15, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  

    class Meta:
        db_table = 'GENRES_PROPRIETES'

class Membres(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=10, unique=True)  
    bur_code = models.ForeignKey(Bureaux, on_delete=models.CASCADE, to_field='code',db_column='BUR_CODE')
    no_certificat = models.CharField(db_column='NO_CERTIFICAT', max_length=15, blank=True, null=True)  
    type_certificat = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_CERTIFICAT_MEMBRE',db_column='TYPE_CERTIFICAT')  
    nom = models.CharField(db_column='NOM', max_length=40, blank=True, null=True)  
    prenom = models.CharField(db_column='PRENOM', max_length=40, blank=True, null=True)  
    titre_professionnel = models.CharField(db_column='TITRE_PROFESSIONNEL', max_length=50, blank=True, null=True)  
    champ_inutilise_1 = models.CharField(db_column='CHAMP_INUTILISE_1', max_length=10, blank=True, null=True)  
    telephone_1 = models.CharField(db_column='TELEPHONE_1', max_length=20, blank=True, null=True)  
    telephone_2 = models.CharField(db_column='TELEPHONE_2', max_length=20, blank=True, null=True)  
    telephone_fax = models.CharField(db_column='TELEPHONE_FAX', max_length=20, blank=True, null=True)  
    courriel = models.CharField(db_column='COURRIEL', max_length=150, blank=True, null=True)  
    site_web = models.CharField(db_column='SITE_WEB', max_length=150, blank=True, null=True)  
    champ_inutilise_2 = models.CharField(db_column='CHAMP_INUTILISE_2', max_length=20, blank=True, null=True)  
    code_langue = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='CODE_LANGUE', db_column='CODE_LANGUE')
    photo_url = models.CharField(db_column='PHOTO_URL', max_length=255, blank=True, null=True)  
    date_modification = models.CharField(db_column='DATE_MODIFICATION', max_length=255, blank=True, null=True)  
    nom_societe = models.CharField(db_column='NOM_SOCIETE', max_length=80, blank=True, null=True)  
    type_societe_desc_f = models.CharField(db_column='TYPE_SOCIETE_DESC_F', max_length=80, blank=True, null=True)  
    type_societe_desc_a = models.CharField(db_column='TYPE_SOCIETE_DESC_A', max_length=80, blank=True, null=True)  
    lien_video_f = models.CharField(db_column='LIEN_VIDEO_F', max_length=255, blank=True, null=True)  
    lien_video_a = models.CharField(db_column='LIEN_VIDEO_A', max_length=255, blank=True, null=True)  
    presentation_f = models.CharField(db_column='PRESENTATION_F', max_length=2000, blank=True, null=True)  
    presentation_a = models.CharField(db_column='PRESENTATION_A', max_length=2000, blank=True, null=True)
    origin = models.CharField(max_length=10,default="Centris")

    class Meta:
        db_table = 'MEMBRES'

class Inscriptions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.CharField(db_column='NO_INSCRIPTION', max_length=14, unique=True)  
    champ_inutilise_1 = models.CharField(db_column='CHAMP_INUTILISE_1', max_length=10, blank=True, null=True)  
    courtier_inscripteur_1 = models.ForeignKey(Membres, on_delete=models.CASCADE, to_field='code', related_name='inscriptions_courtier_1', db_column='COURTIER_INSCRIPTEUR_1', blank=True, null=True)  
    bureau_inscripteur_1 = models.ForeignKey(Bureaux, on_delete=models.CASCADE, to_field='code', related_name='inscriptions_bureau_1', db_column='BUREAU_INSCRIPTEUR_1',blank=True, null=True)
    courtier_inscripteur_2 = models.ForeignKey(Membres, on_delete=models.CASCADE, to_field='code', related_name='inscriptions_courtier_2', db_column='COURTIER_INSCRIPTEUR_2', blank=True, null=True)  
    bureau_inscripteur_2 = models.ForeignKey(Bureaux, on_delete=models.CASCADE, to_field='code', related_name='inscriptions_bureau_2', db_column='BUREAU_INSCRIPTEUR_2',blank=True, null=True)
    prix_demande = models.FloatField(db_column='PRIX_DEMANDE', blank=True, null=True)
    um_prix_demande = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_PRIX', db_column='UM_PRIX_DEMANDE', blank=True, null=True)  
    devise_prix_demande = models.CharField(db_column='DEVISE_PRIX_DEMANDE', max_length=10, blank=True, null=True)  
    prix_location_demande = models.FloatField(db_column='PRIX_LOCATION_DEMANDE', blank=True, null=True)  
    um_prix_location_demande = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='um_prix_location_demande', db_column='UM_PRIX_LOCATION_DEMANDE', blank=True, null=True)  
    devise_prix_location_demande = models.CharField(db_column='DEVISE_PRIX_LOCATION_DEMANDE', max_length=10, blank=True, null=True)  
    champ_inutilise_36 = models.CharField(db_column='CHAMP_INUTILISE_36', max_length=1, blank=True, null=True)  
    code_declaration_vendeur = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='CODE_DECLARATION_VENDEUR',db_column='CODE_DECLARATION_VENDEUR', blank=True, null=True)  
    ind_reprise_finance = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='IND_REPRISE_FINANCE', db_column='IND_REPRISE_FINANCE', blank=True, null=True)
    ind_internet = models.CharField(db_column='IND_INTERNET', max_length=1, blank=True, null=True)  
    ind_echange_possible = models.CharField(db_column='IND_ECHANGE_POSSIBLE', max_length=1, blank=True, null=True)  
    champ_inutilise_37 = models.CharField(db_column='CHAMP_INUTILISE_37', max_length=30, blank=True, null=True)  
    champ_inutilise_3 = models.CharField(db_column='CHAMP_INUTILISE_3', max_length=30, blank=True, null=True)  
    champ_inutilise_4 = models.CharField(db_column='CHAMP_INUTILISE_4', max_length=30, blank=True, null=True)  
    date_mise_en_vigueur = models.DateField(db_column='DATE_MISE_EN_VIGUEUR', blank=True, null=True)  
    champ_inutilise_38 = models.CharField(db_column='CHAMP_INUTILISE_38', max_length=30, blank=True, null=True)  
    mun_code = models.ForeignKey(Municipalites, on_delete=models.CASCADE, to_field='code', db_column='MUN_CODE')  
    quartr_code = models.ForeignKey(Quartiers, on_delete=models.CASCADE, related_name='quartiers_code', db_column='QUARTR_CODE', blank=True, null=True)  
    pres_de = models.CharField(db_column='PRES_DE', max_length=60, blank=True, null=True)  
    no_civique_debut = models.CharField(db_column='NO_CIVIQUE_DEBUT', max_length=10, blank=True, null=True)  
    no_civique_fin = models.CharField(db_column='NO_CIVIQUE_FIN', max_length=10, blank=True, null=True)  
    nom_rue_complet = models.CharField(db_column='NOM_RUE_COMPLET', max_length=60, blank=True, null=True)  
    appartement = models.CharField(db_column='APPARTEMENT', max_length=8, blank=True, null=True)  
    code_postal = models.CharField(db_column='CODE_POSTAL', max_length=6, blank=True, null=True)  
    champ_inutilise_39 = models.CharField(db_column='CHAMP_INUTILISE_39', max_length=30, blank=True, null=True)  
    champ_inutilise_40 = models.CharField(db_column='CHAMP_INUTILISE_40', max_length=30, blank=True, null=True)  
    champ_inutilise_41 = models.CharField(db_column='CHAMP_INUTILISE_41', max_length=30, blank=True, null=True)  
    champ_inutilise_5 = models.CharField(db_column='CHAMP_INUTILISE_5', max_length=30, blank=True, null=True)  
    champ_inutilise_6 = models.CharField(db_column='CHAMP_INUTILISE_6', max_length=30, blank=True, null=True)  
    champ_inutilise_7 = models.CharField(db_column='CHAMP_INUTILISE_7', max_length=30, blank=True, null=True)  
    champ_inutilise_8 = models.CharField(db_column='CHAMP_INUTILISE_8', max_length=30, blank=True, null=True)  
    champ_inutilise_9 = models.CharField(db_column='CHAMP_INUTILISE_9', max_length=30, blank=True, null=True)  
    champ_inutilise_10 = models.CharField(db_column='CHAMP_INUTILISE_10', max_length=30, blank=True, null=True)  
    champ_inutilise_11 = models.CharField(db_column='CHAMP_INUTILISE_11', max_length=30, blank=True, null=True)  
    champ_inutilise_12 = models.CharField(db_column='CHAMP_INUTILISE_12', max_length=30, blank=True, null=True)  
    champ_inutilise_13 = models.CharField(db_column='CHAMP_INUTILISE_13', max_length=30, blank=True, null=True)  
    champ_inutilise_14 = models.CharField(db_column='CHAMP_INUTILISE_14', max_length=30, blank=True, null=True)  
    date_occupation = models.DateField(db_column='DATE_OCCUPATION', blank=True, null=True)  
    delai_occupation_francais = models.CharField(db_column='DELAI_OCCUPATION_FRANCAIS', max_length=15, blank=True, null=True)  
    delai_occupation_anglais = models.CharField(db_column='DELAI_OCCUPATION_ANGLAIS', max_length=15, blank=True, null=True)  
    champ_inutilise_42 = models.CharField(db_column='CHAMP_INUTILISE_42', max_length=30, blank=True, null=True)  
    champ_inutilise_43 = models.CharField(db_column='CHAMP_INUTILISE_43', max_length=30, blank=True, null=True)  
    champ_inutilise_44 = models.CharField(db_column='CHAMP_INUTILISE_44', max_length=30, blank=True, null=True)  
    date_fin_bail = models.DateField(db_column='DATE_FIN_BAIL', blank=True, null=True)  
    champ_inutilise_52 = models.CharField(db_column='CHAMP_INUTILISE_52', max_length=30, blank=True, null=True)  
    champ_inutilise_15 = models.CharField(db_column='CHAMP_INUTILISE_15', max_length=30, blank=True, null=True)  
    champ_inutilise_45 = models.CharField(db_column='CHAMP_INUTILISE_45', max_length=30, blank=True, null=True)  
    categorie_propriete = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='CATEGORIE_PROPRIETE', db_column='CATEGORIE_PROPRIETE',blank=True, null=True)  
    genre_propriete = models.ForeignKey(GenresProprietes, on_delete=models.CASCADE, to_field='genre_propriete' ,db_column='GENRE_PROPRIETE',blank=True, null=True)  
    type_batiment = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_BATIMENT',db_column='TYPE_BATIMENT', blank=True, null=True)  
    type_copropriete = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_COPROPRIETE', db_column='TYPE_COPROPRIETE', blank=True, null=True)  
    niveau = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='NIVEAU', db_column='NIVEAU', max_length=10, blank=True, null=True)  
    nb_etages = models.SmallIntegerField(db_column='NB_ETAGES', blank=True, null=True)  
    annee_contruction = models.CharField(db_column='ANNEE_CONTRUCTION', max_length=4, blank=True, null=True)  
    code_annee_construction = models.CharField(db_column='CODE_ANNEE_CONSTRUCTION', max_length=10, blank=True, null=True)  
    champ_inutilise_16 = models.CharField(db_column='CHAMP_INUTILISE_16', max_length=30, blank=True, null=True)  
    facade_batiment = models.FloatField(db_column='FACADE_BATIMENT', blank=True, null=True)  
    profondeur_batiment = models.FloatField(db_column='PROFONDEUR_BATIMENT', blank=True, null=True)  
    ind_irregulier_batiment = models.CharField(db_column='IND_IRREGULIER_BATIMENT', max_length=1, blank=True, null=True)  
    um_dimension_batiment = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_DIMENSION_BATIMEN',db_column='UM_DIMENSION_BATIMENT', blank=True, null=True)  
    superficie_batiment = models.FloatField(db_column='SUPERFICIE_BATIMENT', blank=True, null=True)  
    um_superficie_batiment = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='um_superficie_batiment', db_column='UM_SUPERFICIE_BATIMENT', blank=True, null=True)  
    superficie_habitable = models.FloatField(db_column='SUPERFICIE_HABITABLE', blank=True, null=True)  
    um_superficie_habitable = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_AIRE_BATIMENT',db_column='UM_SUPERFICIE_HABITABLE', blank=True, null=True)  
    champ_inutilise_17 = models.CharField(db_column='CHAMP_INUTILISE_17', max_length=30, blank=True, null=True)  
    facade_terrain = models.FloatField(db_column='FACADE_TERRAIN', blank=True, null=True)  
    profondeur_terrain = models.FloatField(db_column='PROFONDEUR_TERRAIN', blank=True, null=True)  
    ind_irregulier_terrain = models.CharField(db_column='IND_IRREGULIER_TERRAIN', max_length=1, blank=True, null=True)  
    um_dimension_terrain = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_DIMENSION_TERRAIN', db_column='UM_DIMENSION_TERRAIN', blank=True, null=True)  
    superficie_terrain = models.FloatField(db_column='SUPERFICIE_TERRAIN', blank=True, null=True)  
    um_superficie_terrain = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_SUPERFICIE_TERRAIN',db_column='UM_SUPERFICIE_TERRAIN', blank=True, null=True)  
    champ_inutilise_46 = models.CharField(db_column='CHAMP_INUTILISE_46', max_length=30, blank=True, null=True)  
    annee_evaluation = models.CharField(db_column='ANNEE_EVALUATION', max_length=4, blank=True, null=True)  
    evaluation_municipale_terrain = models.IntegerField(db_column='EVALUATION_MUNICIPALE_TERRAIN', blank=True, null=True)  
    evaluation_municipale_batiment = models.IntegerField(db_column='EVALUATION_MUNICIPALE_BATIMENT', blank=True, null=True)  
    nb_pieces = models.SmallIntegerField(db_column='NB_PIECES', blank=True, null=True)  
    nb_chambres = models.SmallIntegerField(db_column='NB_CHAMBRES', blank=True, null=True)  
    nb_chambres_sous_sol = models.SmallIntegerField(db_column='NB_CHAMBRES_SOUS_SOL', blank=True, null=True)  
    nb_chambres_hors_sol = models.SmallIntegerField(db_column='NB_CHAMBRES_HORS_SOL', blank=True, null=True)  
    nb_salles_bains = models.SmallIntegerField(db_column='NB_SALLES_BAINS', blank=True, null=True)  
    nb_salles_eau = models.SmallIntegerField(db_column='NB_SALLES_EAU', blank=True, null=True)  
    champ_inutilise_47 = models.CharField(db_column='CHAMP_INUTILISE_47', max_length=30, blank=True, null=True)  
    champ_inutilise_48 = models.CharField(db_column='CHAMP_INUTILISE_48', max_length=30, blank=True, null=True)  
    champ_inutilise_18 = models.CharField(db_column='CHAMP_INUTILISE_18', max_length=30, blank=True, null=True)  
    champ_inutilise_19 = models.CharField(db_column='CHAMP_INUTILISE_19', max_length=30, blank=True, null=True)  
    champ_inutilise_20 = models.CharField(db_column='CHAMP_INUTILISE_20', max_length=30, blank=True, null=True)  
    champ_inutilise_21 = models.CharField(db_column='CHAMP_INUTILISE_21', max_length=30, blank=True, null=True)  
    depenses_tot_exploitation = models.IntegerField(db_column='DEPENSES_TOT_EXPLOITATION', blank=True, null=True)  
    champ_inutilise_22 = models.CharField(db_column='CHAMP_INUTILISE_22', max_length=30, blank=True, null=True)  
    champ_inutilise_23 = models.CharField(db_column='CHAMP_INUTILISE_23', max_length=30, blank=True, null=True)  
    nom_plan_eau = models.CharField(db_column='NOM_PLAN_EAU', max_length=50, blank=True, null=True)  
    champ_inutilise_24 = models.CharField(db_column='CHAMP_INUTILISE_24', max_length=30, blank=True, null=True)  
    champ_inutilise_25 = models.CharField(db_column='CHAMP_INUTILISE_25', max_length=30, blank=True, null=True)  
    nb_chauffe_eau_loue = models.SmallIntegerField(db_column='NB_CHAUFFE_EAU_LOUE', blank=True, null=True)  
    inclus_francais = models.TextField(db_column='INCLUS_FRANCAIS', max_length=250, blank=True, null=True)  
    inclus_anglais = models.TextField(db_column='INCLUS_ANGLAIS', max_length=250, blank=True, null=True)  
    exclus_francais = models.TextField(db_column='EXCLUS_FRANCAIS', max_length=250, blank=True, null=True)  
    exclus_anglais = models.TextField(db_column='EXCLUS_ANGLAIS', max_length=250, blank=True, null=True)  
    nb_unites_total = models.SmallIntegerField(db_column='NB_UNITES_TOTAL', blank=True, null=True)  
    champ_inutilise_26 = models.CharField(db_column='CHAMP_INUTILISE_26', max_length=30, blank=True, null=True)  
    champ_inutilise_27 = models.CharField(db_column='CHAMP_INUTILISE_27', max_length=30, blank=True, null=True)  
    champ_inutilise_28 = models.CharField(db_column='CHAMP_INUTILISE_28', max_length=30, blank=True, null=True)  
    champ_inutilise_29 = models.CharField(db_column='CHAMP_INUTILISE_29', max_length=30, blank=True, null=True)  
    champ_inutilise_30 = models.CharField(db_column='CHAMP_INUTILISE_30', max_length=30, blank=True, null=True)  
    champ_inutilise_31 = models.CharField(db_column='CHAMP_INUTILISE_31', max_length=30, blank=True, null=True)  
    champ_inutilise_32 = models.CharField(db_column='CHAMP_INUTILISE_32', max_length=30, blank=True, null=True)  
    champ_inutilise_49 = models.CharField(db_column='CHAMP_INUTILISE_49', max_length=30, blank=True, null=True)  
    date_modif = models.DateTimeField(db_column='DATE_MODIF', blank=True, null=True)
    frequence_prix_location = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='FREQUENCE_PRIX_LOCATION', db_column='FREQUENCE_PRIX_LOCATION', blank=True, null=True)  
    code_statut = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='CODE_STATUT', db_column='CODE_STATUT')
    pourc_quote_part = models.FloatField(db_column='POURC_QUOTE_PART', blank=True, null=True)  
    utilisation_commerciale = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UTILISATION_COMMERCIALE',db_column='UTILISATION_COMMERCIALE',  blank=True, null=True)
    champ_inutilise_2 = models.CharField(db_column='CHAMP_INUTILISE_2', max_length=30, blank=True, null=True)  
    nom_du_parc = models.CharField(db_column='NOM_DU_PARC', max_length=30, blank=True, null=True)  
    champ_inutilise_50 = models.CharField(db_column='CHAMP_INUTILISE_50', max_length=30, blank=True, null=True)  
    champ_inutilise_51 = models.CharField(db_column='CHAMP_INUTILISE_51', max_length=30, blank=True, null=True)  
    raison_sociale = models.CharField(db_column='RAISON_SOCIALE', max_length=40, blank=True, null=True)  
    en_oper_depuis = models.CharField(db_column='EN_OPER_DEPUIS', max_length=6, blank=True, null=True)  
    ind_franchise = models.CharField(db_column='IND_FRANCHISE', max_length=1, blank=True, null=True)  
    champ_inutilise_33 = models.CharField(db_column='CHAMP_INUTILISE_33', max_length=30, blank=True, null=True)  
    champ_inutilise_34 = models.CharField(db_column='CHAMP_INUTILISE_34', max_length=30, blank=True, null=True)  
    champ_inutilise_35 = models.CharField(db_column='CHAMP_INUTILISE_35', max_length=30, blank=True, null=True)  
    ind_opt_renouv_bail = models.CharField(db_column='IND_OPT_RENOUV_BAIL', max_length=1, blank=True, null=True)  
    annee_mois_echeance_bail = models.CharField(db_column='ANNEE_MOIS_ECHEANCE_BAIL', max_length=6, blank=True, null=True)  
    url_visite_virtuelle_francais = models.CharField(db_column='URL_VISITE_VIRTUELLE_FRANCAIS', max_length=150, blank=True, null=True)  
    url_visite_virtuelle_anglais = models.CharField(db_column='URL_VISITE_VIRTUELLE_ANGLAIS', max_length=150, blank=True, null=True)  
    url_desc_detaillee = models.CharField(db_column='URL_DESC_DETAILLEE', max_length=180, blank=True, null=True)  
    ind_taxes_prix_demande = models.CharField(db_column='IND_TAXES_PRIX_DEMANDE', max_length=1, blank=True, null=True)  
    ind_taxes_prix_location_demande = models.CharField(db_column='IND_TAXES_PRIX_LOCATION_DEMANDE', max_length=1, blank=True, null=True)  
    courtier_inscripteur_3 = models.CharField(db_column='COURTIER_INSCRIPTEUR_3', max_length=255, blank=True, null=True)  
    bureau_inscripteur_3 = models.CharField(db_column='BUREAU_INSCRIPTEUR_3', max_length=255, blank=True, null=True)  
    courtier_inscripteur_4 = models.CharField(db_column='COURTIER_INSCRIPTEUR_4', max_length=255, blank=True, null=True)  
    bureau_inscripteur_4 = models.CharField(db_column='BUREAU_INSCRIPTEUR_4', max_length=255, blank=True, null=True)  
    courtier1_type_divul_interet = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='courtier1_type_divul_interet', db_column='COURTIER1_TYPE_DIVUL_INTERET', blank=True, null=True)
    courtier2_type_divul_interet = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='courtier2_type_divul_interet', db_column='COURTIER2_TYPE_DIVUL_INTERET', blank=True, null=True)
    courtier3_type_divul_interet = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='courtier3_type_divul_interet', db_column='COURTIER3_TYPE_DIVUL_INTERET', blank=True, null=True)
    courtier4_type_divul_interet = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='courtier4_type_divul_interet', db_column='COURTIER4_TYPE_DIVUL_INTERET', blank=True, null=True)
    ind_vente_sans_garantie_legale = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='ind_vente_sans_garantie_legale', db_column='IND_VENTE_SANS_GARANTIE_LEGALE', blank=True, null=True)  
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  
    type_superficie_habitable = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_SUPERFICIE_HABITABLE', db_column='TYPE_SUPERFICIE_HABITABLE', blank=True, null=True)  
    rev_pot_brut_res = models.IntegerField(db_column='REV_POT_BRUT_RES', blank=True, null=True)  
    rev_pot_brut_comm = models.IntegerField(db_column='REV_POT_BRUT_COMM', blank=True, null=True)  
    rev_pot_brut_stat = models.IntegerField(db_column='REV_POT_BRUT_STAT', blank=True, null=True)  
    rev_pot_brut_au = models.IntegerField(db_column='REV_POT_BRUT_AU', blank=True, null=True)  
    date_rev_brut_pot = models.DateField(db_column='DATE_REV_BRUT_POT', blank=True, null=True)  
    particularite_construction = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='PARTICULARITE_CONSTRUCTION', db_column='PARTICULARITE_CONSTRUCTION', blank=True, null=True)
    au_genre_propriete_info_f = models.CharField(db_column='AU_GENRE_PROPRIETE_INFO_F', max_length=255, blank=True, null=True)  
    au_genre_propriete_info_a = models.CharField(db_column='AU_GENRE_PROPRIETE_INFO_A', max_length=255, blank=True, null=True)  
    prix_demande_taxe_incl = models.IntegerField(db_column='PRIX_DEMANDE_TAXE_INCL', blank=True, null=True)  
    ind_visites_interactive = models.CharField(db_column='IND_VISITES_INTERACTIVE', max_length=255, blank=True, null=True)  
    addenda_complet_f = models.TextField(db_column='ADDENDA_COMPLET_F', blank=True, null=True)
    addenda_complet_a = models.TextField(db_column='ADDENDA_COMPLET_A', blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'INSCRIPTIONS'
    
    def __str__(self):
        return self.no_inscription

class Addenda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, to_field='no_inscription', related_name='no_inscription_addenda', db_column='NO_INSCRIPTION')  
    no_addenda = models.SmallIntegerField(db_column='NO_ADDENDA', blank=False, null=False)  
    code_langue = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='code_langue', db_column='CODE_LANGUE')  
    ordre_affichage = models.SmallIntegerField(db_column='ORDRE_AFFICHAGE', blank=False, null=False)  
    champ_inutilise_1 = models.CharField(db_column='CHAMP_INUTILISE_1', max_length=3, blank=True, null=True)  
    champ_inutilise_2 = models.CharField(db_column='CHAMP_INUTILISE_2', max_length=3, blank=True, null=True)  
    texte = models.CharField(db_column='TEXTE', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'ADDENDA'

class TypeCaracteristiques(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(db_column='CODE', max_length=4, unique=True)  
    description_abregee_francaise = models.CharField(db_column='DESCRIPTION_ABREGEE_FRANCAISE', max_length=15, blank=True, null=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_abregee_anglaise = models.CharField(db_column='DESCRIPTION_ABREGEE_ANGLAISE', max_length=15, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  
    ind_plusieurs_criteres = models.CharField(db_column='IND_PLUSIEURS_CRITERES', max_length=1, blank=True, null=True)  

    class Meta:
        db_table = 'TYPE_CARACTERISTIQUES'

class SousTypeCaracteristiques(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tcar_code = models.ForeignKey(TypeCaracteristiques, on_delete=models.CASCADE, to_field='code', db_column='TCAR_CODE')
    code = models.CharField(db_column='CODE', max_length=4, unique=False)  
    description_abregee_francaise = models.CharField(db_column='DESCRIPTION_ABREGEE_FRANCAISE', max_length=15, blank=True, null=True)  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_abregee_anglaise = models.CharField(db_column='DESCRIPTION_ABREGEE_ANGLAISE', max_length=15, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  

    class Meta:
        db_table = 'SOUS_TYPE_CARACTERISTIQUES'

class Caracteristiques(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='caracteristiques', db_column='NO_INSCRIPTION')
    tcar_code = models.ForeignKey(TypeCaracteristiques, on_delete=models.CASCADE, to_field='code', db_column='TCAR_CODE', blank=True, null=True)  
    scarac_code = models.ForeignKey(SousTypeCaracteristiques, on_delete=models.CASCADE, db_column='SCARAC_CODE')  
    nombre = models.SmallIntegerField(db_column='NOMBRE', blank=True, null=True)  
    informations_francaises = models.CharField(db_column='INFORMATIONS_FRANCAISES', max_length=60, blank=True, null=True)  
    informations_anglaises = models.CharField(db_column='INFORMATIONS_ANGLAISES', max_length=60, blank=True, null=True)  
    montant = models.IntegerField(db_column='MONTANT', blank=True, null=True)  

    class Meta:
        db_table = 'CARACTERISTIQUES'

class Depenses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='depenses', db_column='NO_INSCRIPTION')
    tdep_code = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_DEPENSE',db_column='TDEP_CODE')  
    montant_depense = models.IntegerField(db_column='MONTANT_DEPENSE', blank=True, null=True)  
    annee = models.SmallIntegerField(db_column='ANNEE', blank=True, null=True)  
    annee_expiration = models.SmallIntegerField(db_column='ANNEE_EXPIRATION', blank=True, null=True)  
    frequence = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='frequence', db_column='FREQUENCE')  
    part_depense = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='part_depense', db_column='PART_DEPENSE')  
    au_depense_info_f = models.CharField(db_column='AU_DEPENSE_INFO_F', max_length=255, blank=True, null=True)  
    au_depense_info_a = models.CharField(db_column='AU_DEPENSE_INFO_A', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'DEPENSES'

class LiensAdditionnels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='liensAdditionnels', db_column='NO_INSCRIPTION')  
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    type_lien = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='type_lien', db_column='TYPE_LIEN')  
    lien_francais = models.CharField(db_column='LIEN_FRANCAIS', max_length=255, blank=True, null=True)  
    lien_anglais = models.CharField(db_column='LIEN_ANGLAIS', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'LIENS_ADDITIONNELS'

class MembresMediasSociaux(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    membre_code = models.ForeignKey(Membres, on_delete=models.CASCADE, to_field='code', db_column='MEMBRE_CODE') 
    type_media_social = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_MEDIA_SOCIAL',db_column='TYPE_MEDIA_SOCIAL')  
    lien_media_social = models.CharField(db_column='LIEN_MEDIA_SOCIAL', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'MEMBRES_MEDIAS_SOCIAUX'

class Photos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='photos', db_column='NO_INSCRIPTION')
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    nom_fichier_photo = models.CharField(db_column='NOM_FICHIER_PHOTO', max_length=20, blank=True, null=True)  
    code_description_photo = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='code_description_photo',db_column='CODE_DESCRIPTION_PHOTO')  
    description_francaise = models.CharField(db_column='DESCRIPTION_FRANCAISE', max_length=60, blank=True, null=True)  
    description_anglaise = models.CharField(db_column='DESCRIPTION_ANGLAISE', max_length=60, blank=True, null=True)  
    photourl = models.CharField(db_column='PhotoURL', max_length=255, blank=True, null=True)  
    no_version = models.CharField(db_column='NO_VERSION', max_length=255, blank=True, null=True)  
    date_modification = models.CharField(db_column='DATE_MODIFICATION', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'PHOTOS'

class PiecesUnites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='piecesUnites', db_column='NO_INSCRIPTION')
    seq_unite_det = models.SmallIntegerField(db_column='SEQ_UNITE_DET', blank=True, null=True)  
    seq = models.IntegerField(db_column='SEQ', blank=True, null=True)  
    piece_code = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='piece_code', db_column='PIECE_CODE', blank=True, null=True)  
    au_piece_info_f = models.CharField(db_column='AU_PIECE_INFO_F', max_length=50, blank=True, null=True)  
    au_piece_info_a = models.CharField(db_column='AU_PIECE_INFO_A', max_length=50, blank=True, null=True)  
    niveau = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='niveau_pieces_unites', db_column='NIVEAU')  
    au_niveau_info_f = models.CharField(db_column='AU_NIVEAU_INFO_F', max_length=50, blank=True, null=True)  
    au_niveau_info_a = models.CharField(db_column='AU_NIVEAU_INFO_A', max_length=50, blank=True, null=True)  
    dimensions = models.CharField(db_column='DIMENSIONS', max_length=15, blank=True, null=True)  
    ind_irregulier = models.CharField(db_column='IND_IRREGULIER', max_length=1, blank=True, null=True)  
    couvre_plancher_code = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='couvre_plancher_code', db_column='COUVRE_PLANCHER_CODE', blank=True, null=True)  
    au_couvre_plancher_f = models.CharField(db_column='AU_COUVRE_PLANCHER_F', max_length=50, blank=True, null=True)  
    au_couvre_plancher_a = models.CharField(db_column='AU_COUVRE_PLANCHER_A', max_length=50, blank=True, null=True)  
    ind_foyer_poele = models.CharField(db_column='IND_FOYER_POELE', max_length=255, blank=True, null=True)  
    info_supp_f = models.CharField(db_column='INFO_SUPP_F', max_length=30, blank=True, null=True)  
    info_supp_a = models.CharField(db_column='INFO_SUPP_A', max_length=30, blank=True, null=True)  

    class Meta:
        db_table = 'PIECES_UNITES'

class Remarques(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='remarques', db_column='NO_INSCRIPTION')  
    no_remarque = models.SmallIntegerField(db_column='NO_REMARQUE', blank=True, null=True)  
    code_langue = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='code_langue_remarques', db_column='CODE_LANGUE')  
    ordre_affichage = models.SmallIntegerField(db_column='ORDRE_AFFICHAGE', blank=True, null=True)  
    champ_inutilise_1 = models.CharField(db_column='CHAMP_INUTILISE_1', max_length=1, blank=True, null=True)  
    champ_inutilise_2 = models.CharField(db_column='CHAMP_INUTILISE_2', max_length=1, blank=True, null=True)  
    texte = models.TextField(db_column='TEXTE', blank=True, null=True)  

    class Meta:
        db_table = 'REMARQUES'

class Renovations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='renovations', db_column='NO_INSCRIPTION')
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    renovation_type = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='renovation_type',db_column='RENOVATION_TYPE')  
    annee = models.SmallIntegerField(db_column='ANNEE', blank=True, null=True)  
    champ_inutilise_1 = models.SmallIntegerField(db_column='CHAMP_INUTILISE_1', blank=True, null=True)  
    informations_francaises = models.CharField(db_column='INFORMATIONS_FRANCAISES', max_length=30, blank=True, null=True)  
    informations_anglaises = models.CharField(db_column='INFORMATIONS_ANGLAISES', max_length=30, blank=True, null=True)  
    montant = models.IntegerField(db_column='MONTANT', blank=True, null=True)  

    class Meta:
        db_table = 'RENOVATIONS'

class UnitesDetaillees(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, to_field='no_inscription', db_column='NO_INSCRIPTION') 
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    type_unite_det = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='TYPE_UNITE_DET', db_column='TYPE_UNITE_DET', blank=True, null=True)  
    nb_pieces = models.SmallIntegerField(db_column='NB_PIECES', blank=True, null=True)
    nb_chambres = models.SmallIntegerField(db_column='NB_CHAMBRES', blank=True, null=True)  
    inclus_chauffage = models.CharField(db_column='INCLUS_CHAUFFAGE', max_length=10, blank=True, null=True)  
    inclus_electricite = models.CharField(db_column='INCLUS_ELECTRICITE', max_length=1, blank=True, null=True)  
    inclus_eau_chaude = models.CharField(db_column='INCLUS_EAU_CHAUDE', max_length=1, blank=True, null=True)  
    inclus_taxe_eau = models.CharField(db_column='INCLUS_TAXE_EAU', max_length=255, blank=True, null=True)  
    inclus_pelouse = models.CharField(db_column='INCLUS_PELOUSE', max_length=10, blank=True, null=True)  
    inclus_deneigement = models.CharField(db_column='INCLUS_DENEIGEMENT', max_length=15, blank=True, null=True)  
    inclus_meuble = models.CharField(db_column='INCLUS_MEUBLE', max_length=1, blank=True, null=True)  
    inclus_semi_meuble = models.CharField(db_column='INCLUS_SEMI_MEUBLE', max_length=1, blank=True, null=True)  
    nb_stat_interieurs = models.CharField(db_column='NB_STAT_INTERIEURS', max_length=5, blank=True, null=True)  
    nb_stat_exterieurs = models.CharField(db_column='NB_STAT_EXTERIEURS', max_length=5, blank=True, null=True)  
    au_inclus_info_f = models.CharField(db_column='AU_INCLUS_INFO_F', max_length=50, blank=True, null=True)  
    au_inclus_info_a = models.CharField(db_column='AU_INCLUS_INFO_A', max_length=50, blank=True, null=True)  
    ind_vacant = models.CharField(db_column='IND_VACANT', max_length=255, blank=True, null=True)  
    superficie_totale = models.CharField(db_column='SUPERFICIE_TOTALE', max_length=8, blank=True, null=True)  
    um_superficie_totale = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='UM_SUPERFICIE_TOTALE',db_column='UM_SUPERFICIE_TOTALE', blank=True, null=True)

    class Meta:
        db_table = 'UNITES_DETAILLEES'

class UnitesSommaires(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='TYPE_UNITE_SOM', db_column='NO_INSCRIPTION') 
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    type_unite_som = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='type_unite_som', db_column='TYPE_UNITE_SOM', blank=True, null=True)  
    nb_total_unites = models.SmallIntegerField(db_column='NB_TOTAL_UNITES', blank=True, null=True)  
    nb_unites_vacantes = models.SmallIntegerField(db_column='NB_UNITES_VACANTES', blank=True, null=True)  
    au_unite_revenu_info_f = models.CharField(db_column='AU_UNITE_REVENU_INFO_F', max_length=60, blank=True, null=True)  
    au_unite_revenu_info_a = models.CharField(db_column='AU_UNITE_REVENU_INFO_A', max_length=60, blank=True, null=True)  

    class Meta:
        db_table = 'UNITES_SOMMAIRES'

class VisitesLibres(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_inscription = models.ForeignKey(Inscriptions, on_delete=models.CASCADE, related_name='no_inscription_visites_libres', db_column='NO_INSCRIPTION') 
    seq = models.SmallIntegerField(db_column='SEQ', blank=True, null=True)  
    date_debut = models.CharField(db_column='DATE_DEBUT', max_length=10, blank=True, null=True)  
    date_fin = models.CharField(db_column='DATE_FIN', max_length=10, blank=True, null=True)  
    heure_debut = models.CharField(db_column='HEURE_DEBUT', max_length=5, blank=True, null=True)  
    heure_fin = models.CharField(db_column='HEURE_FIN', max_length=5, blank=True, null=True)  
    commentaires_f = models.CharField(db_column='COMMENTAIRES_F', max_length=60, blank=True, null=True)  
    commentaires_a = models.CharField(db_column='COMMENTAIRES_A', max_length=60, blank=True, null=True)  
    code_visite_caravane = models.ForeignKey(ValeursFixes, on_delete=models.CASCADE, related_name='CODE_VISITE_CARAVANE', db_column='CODE_VISITE_CARAVANE')  
    lien_visite_virt = models.CharField(db_column='LIEN_VISITE_VIRT', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'VISITES_LIBRES' 