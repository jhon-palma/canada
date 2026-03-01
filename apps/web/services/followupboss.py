import pdb

import requests
from django.conf import settings


BROKER_ID_MAP = {
    'Alexandra Ross':6,
    'Marina Kozokar':12,
    'Vanessa Mclarty':15,
    'Amanda Roy':7,
    'Julie-Christine Caban':13,
    'LJ Aguinaga':1
}

class FollowUpBossService:

    BASE_URL = settings.BASE_URL

    @staticmethod
    def send_event(message):
        payload = {
            "source": "Web LJ Realties",
            "type": "General Inquiry",
            "message": message.message,
            "person": {
                "firstName": message.nom,
                "emails": [
                    {"value": message.courriel}
                ],
                "phones": (
                    [{"value": message.telephone}]
                    if message.telephone else []
                ),
                "tags": message.tags
            }
        }

        assigned_user_id = BROKER_ID_MAP.get(message.broker)
        if assigned_user_id:
            payload["assignedUserId"] = assigned_user_id
        
        endpoint = f"events"
        url = f"{FollowUpBossService.BASE_URL}{endpoint.lstrip('/')}"

        response = requests.post(
            url,
            json=payload,
            auth=(settings.FOLLOWUPBOSS_API_KEY, ""),
            timeout=10
        )
        
        data = response.json()

        if response.status_code in [200, 201] and "id" in data:
            message.person_fub_id = data["id"]
            message.save(update_fields=["person_fub_id"])

            assigned_user_id = BROKER_ID_MAP.get(message.broker)

            if assigned_user_id:
                
                update_endpoint = f"people/{data['id']}"
                update_url = f"{FollowUpBossService.BASE_URL}{update_endpoint.lstrip('/')}"

                requests.put(
                    update_url,
                    json={"assignedUserId": assigned_user_id},
                    auth=(settings.FOLLOWUPBOSS_API_KEY, ""),
                    timeout=10
                )

        return response
    
    