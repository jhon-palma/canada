import pdb

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.web.models import Formulaire_contact
from apps.web.services.followupboss import FollowUpBossService


@require_POST
def contact_messages(request):
    try:
        tags_list = request.POST.getlist('tag')

        new = Formulaire_contact.objects.create(
            nom=request.POST.get('prenom'),
            courriel=request.POST.get('email'),
            sujet=request.POST.get('sujet'),
            tags=tags_list if tags_list else [],
            broker=request.POST.get('broker'),
            message=request.POST.get('comment'),
            adresse=request.POST.get('adresse'),
            telephone=request.POST.get('tel'),
        )
        response = FollowUpBossService.send_event(new)

        if response.status_code in [200, 201]:
            data = response.json()
            
            new.is_synced = True
            new.person_fub_id = data.get("id")
            
            new.save(update_fields=["is_synced", "person_fub_id"])
        else:
            new.sync_error = response.text
            new.save(update_fields=["sync_error"])

        return JsonResponse({'response': 1})
    except Exception as e:
        return JsonResponse({
            'response': 0,
            'error': str(e)
        })


