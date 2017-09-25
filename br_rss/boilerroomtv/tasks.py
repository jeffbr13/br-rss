import logging
from datetime import datetime, timedelta

import iso8601
import requests
from django.utils.html import strip_tags
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import Recording, Channel

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


def update_or_create_channel_from_json(channel_json):
    logger.info('Updating/creating channel from <%s>…', channel_json['url'])
    channel, created = Channel.objects.update_or_create(
        id=channel_json['id'],
        url=channel_json['url'],
        web_url='https://boilerroom.tv/channel/%s/' % channel_json['id'],
        defaults=dict(
            title='Channel %s' % channel_json['id'],
            description=channel_json['description'].strip(),
            thumbnail_url=channel_json['logo_image'],
        )
    )
    logger.info(('Created %r.' if created else 'Updated %r.') % channel)
    logger.info('Setting %r featured recordings…', channel)
    featured_playlist_json = requests.get(channel_json['featured_playlist']).json()
    featured_recordings_json = requests.get(featured_playlist_json['recordings']).json()['results']
    featured_recordings = [Recording.objects.get(url=r['url']) for r in featured_recordings_json]
    channel.featured_recordings.set(featured_recordings)
    logger.debug('%r featured recordings are: %r.', channel, featured_recordings)
    logger.info('Set %r featured recordings.', channel)


@db_periodic_task(crontab(minute='10'))
def scrape_channels():
    logger.info('Scraping channels…')
    response = requests.get('https://archive.boilerroom.tv/api/channels/')
    response.raise_for_status()
    for c in response.json()['results']:
        update_or_create_channel_from_json(c)

