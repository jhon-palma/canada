import io
import django
import sys 
import os
import sys
import isodate
from googleapiclient.discovery import build
from django.utils.dateparse import parse_datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immobilier.settings')
django.setup()

from apps.web.models import VideosWeb
from immobilier.local_settings import CHANNEL_ID, KEY_API_YB
from scripts.send_email import sendEmail


FRAGMENTOS_A_ELIMINAR = [
    'https://www.ljrealties.com - Find your future dream home',
    'https://www.ljrealties.com - Trouvez votre future maison de rêve',
    'https://www.ljrealties.com - Trouvez la maison de vos rêves'
]

PALABRA_CLAVE_ELIMINAR = 'LJ Aguinaga'



def clean_description(description):
    for fragmento in FRAGMENTOS_A_ELIMINAR:
        if description.startswith(fragmento):
            description = description[len(fragmento):].strip()

    if PALABRA_CLAVE_ELIMINAR in description:
        description = description.split(PALABRA_CLAVE_ELIMINAR, 1)[0].strip()

    return description



def parse_duration(duration):
    return isodate.parse_duration(duration).total_seconds()



def fetch_videos_from_channel(channel_id):
    videos = []
    next_page_token = None
    youtube = build('youtube', 'v3', developerKey=KEY_API_YB)
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()
    upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
   
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=upload_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_at = parse_datetime(item['snippet']['publishedAt'])

            video_details = youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()

            caption = video_details['items'][0]['contentDetails']['caption']
            duration = video_details['items'][0]['contentDetails']['duration']
            duration_seconds = parse_duration(duration)
            description = clean_description(description)
            is_short = True if duration_seconds <= 61 and caption == 'false' else False

            videos.append({
                'videoId': video_id,
                'tittle': title,
                'description': description,
                'publishedAt': published_at,
                'is_short': is_short
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos



def save_videos_to_db(videos):
    for video in videos:
        obj, created = VideosWeb.objects.update_or_create(
            videoId=video['videoId'],
            defaults={
                'tittle': video['tittle'],
                'description': video['description'],
                'publishedAt': video['publishedAt'],
                'is_short': video['is_short']
            }
        )
        if created:
            print(f"Video '{video['tittle']}' guardado con ID {obj.id}.")
        else:
            print(f"Video '{video['tittle']}' ya existe y fue actualizado.")

    fix_videos = ['Holiday Client Appreciation Dinner','Notre-Dame-de-Grâce | Home For Sale | 611 SQFT | 1 Beds | 1 Bath']
    VideosWeb.objects.filter(tittle__in=fix_videos).update(is_short=False)

    fix_shorts = ['Bank of Canada Rate Increase!!']
    VideosWeb.objects.filter(tittle__in=fix_shorts).update(is_short=True)
    


if __name__ == "__main__":
    channel_id = CHANNEL_ID
    videos = fetch_videos_from_channel(channel_id)
    save_videos_to_db(videos)
    sendEmail('icloudcris@gmail.com', 'backups@remaxplatinum.pe', 'CANADA DOWNLOAD VIDEOS', str(len(videos)))

