from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from .models import Recording, Channel, Genre


def index(request: HttpRequest):
    return render(
        request,
        'index.html',
        context=dict(
            channels=Channel.objects.all(),
            genres=Genre.objects.all(),
        )
    )


def all_recordings_rss(request: HttpRequest):
    server_url = '%s://%s' % (request._get_scheme(), request.get_host())
    return render(
        request,
        'rss.xml',
        context=dict(
            server_url=server_url,
            channel_title='Boiler Room',
            channel_subtitle='Broadcasting the underground.',
            channel_description='Boiler Room televises underground music as it happens from around the world to a '
                                'massive online community. By doing so, we create windows into scenes and sounds from '
                                'every corner of the globe, connecting millions of music heads with the specific '
                                'music they love. This communal participation has redrawn the map for underground '
                                'culture and proven that mass audiences now subscribe to alternative choice.',
            channel_keywords='grime, garage, dubstep, house, techno, music',
            channel_artwork_url=server_url + static('artwork.png'),
            podcasts=Recording.objects.all(),
        ),
        content_type='application/rss+xml',
    )


def channel_rss(request: HttpRequest, channel_id: int):
    channel = get_object_or_404(Channel, pk=channel_id)
    server_url = '%s://%s' % (request._get_scheme(), request.get_host())
    return render(
        request,
        'rss.xml',
        context=dict(
            server_url=server_url,
            channel_title='Boiler Room - %s' % channel.title,
            channel_subtitle=channel.description,
            channel_description=channel.description,
            channel_keywords=channel.keywords,
            channel_artwork_url=channel.thumbnail_url,
            podcasts=channel.featured_recordings.all(),
        ),
        content_type='application/rss+xml',
    )


def genre_rss(request: HttpRequest, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    server_url = '%s://%s' % (request._get_scheme(), request.get_host())
    return render(
        request,
        'rss.xml',
        context=dict(
            server_url=server_url,
            channel_title='Boiler Room - %s' % genre.title,
            channel_description=genre.description,
            channel_keywords='Music, %s' % genre.title,
            channel_artwork_url=server_url + static('artwork.png'),
            podcasts=genre.recordings.all(),
        ),
        content_type='application/rss+xml',
    )
