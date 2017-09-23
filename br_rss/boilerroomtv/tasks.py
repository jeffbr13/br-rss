import logging
from datetime import datetime, timedelta

import iso8601
import requests
from django.utils.html import strip_tags
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import Recording


logger = logging.getLogger(__name__)


def update_or_create_recording_from_json(recording_json):
    if recording_json['audio_file']:
        logger.info('Updating/creating Recording from <%s>…', recording_json['url'])
        d = datetime.strptime(recording_json['duration'], '%H:%M:%S')
        duration = timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
        artists = [requests.get(artist_url).json()['name'] for artist_url in recording_json['artists']]
        audio_response = requests.head(recording_json['audio_file'])
        audio_response.raise_for_status()
        audio_content_type = audio_response.headers['Content-Type']
        audio_content_length = int(audio_response.headers['Content-Length'])
        assert 'audio/' in audio_content_type
        assert audio_content_length > 0
        recording, created = Recording.objects.update_or_create(
            url=recording_json['url'],
            web_url=recording_json['wordpress_permalink_url'],
            defaults=dict(
                title=strip_tags(recording_json['title']).strip(),
                description=strip_tags(recording_json['description']).strip(),
                artists=', '.join(artists),
                released=iso8601.parse_date(recording_json['released']),
                duration=duration,
                thumbnail_url=recording_json.get('thumbnail_image', ''),
                audio_url=recording_json['audio_file'],
                audio_content_type=audio_content_type,
                audio_content_length=audio_content_length,
            )
        )
        logger.info(('Created %r.' if created else 'Updated %r.') % recording)
        return recording, created
    else:
        logger.warning('Skipping <%s>, no audio file.', recording_json['url'])
        return None, False


@db_periodic_task(crontab(minute='0'))
def scrape_latest_recordings():
    logger.info('Scraping latest recordings…')
    response = requests.get('https://archive.boilerroom.tv/api/recordings/')
    response.raise_for_status()
    for r in response.json()['results']:
        update_or_create_recording_from_json(r)
    logger.info('Scraped latest recordings.')


def scrape_all_recordings():
    next_page = 'https://archive.boilerroom.tv/api/recordings/'
    while next_page:
        logger.info('Scraping recordings from <%s>…', next_page)
        response = requests.get(next_page)
        response.raise_for_status()
        for r in response.json()['results']:
            try:
                update_or_create_recording_from_json(r)
            except:
                logger.exception('Issue with recording:')
        logger.info('Scraped recordings from <%s>.', next_page)
        next_page = response.json().get('next')

