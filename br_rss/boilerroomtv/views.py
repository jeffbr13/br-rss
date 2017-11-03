from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from podcast_feed import PodcastFeed

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


class RecordingsPodcastFeed(PodcastFeed):
    itunes_category = 'Music'
    explicit = True
    author_name = 'Boiler Room'
    copyright = 'Boiler Room'
    owner_name = 'Ben Jeffrey'
    owner_email = 'br-rss@jeffbr13.net'

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.web_url

    def item_author_name(self, item):
        return item.artists

    def item_duration(self, item):
        return item.duration

    def item_enclosure_url(self, item):
        return item.audio_url

    def item_enclosure_length(self, item):
        return item.audio_content_length

    def item_enclosure_mime_type(self, item):
        return item.audio_content_type

    def item_pubdate(self, item):
        return item.released


class AllRecordingsPodcastFeed(RecordingsPodcastFeed):
    link = 'https://boilerroom.tv/'
    title = 'Boiler Room'
    subtitle = 'Broadcasting the underground.'
    description = (
        'Boiler Room televises underground music as it happens from around the world to a '
        'massive online community. By doing so, we create windows into scenes and sounds from '
        'every corner of the globe, connecting millions of music heads with the specific '
        'music they love. This communal participation has redrawn the map for underground '
        'culture and proven that mass audiences now subscribe to alternative choice.'
    )
    categories = ('grime', 'garage', 'dubstep', 'house', 'techno', 'music',)
    artwork_link = static('artwork.png')

    def items(self):
        return Recording.objects.all()


class ChannelPodcastFeed(RecordingsPodcastFeed):
    def get_object(self, request, channel_id):
        return Channel.objects.get(id=channel_id)

    def link(self, obj):
        return obj.web_url

    def title(self, obj):
        return 'Boiler Room - %s' % obj.title

    def subtitle(self, obj):
        return obj.description

    def description(self, obj):
        return obj.description

    def categories(self, obj):
        keywords_split = obj.keywords.split(', ')
        return keywords_split

    def artwork_link(self, obj):
        return obj.thumbnail_url

    def items(self, obj):
        return obj.featured_recordings.all()


def genre_rss(request: HttpRequest, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    server_url = '%s://%s' % (request._get_scheme(), request.get_host())
    return render(
        request,
        'rss.xml',
        context=dict(
            server_url=server_url,
            web_link=genre.web_url,
            channel_title='Boiler Room - %s' % genre.title,
            channel_description=genre.description,
            channel_keywords='Music, %s' % genre.title,
            channel_artwork_url=server_url + static('artwork.png'),
            podcasts=genre.recordings.all(),
        ),
        content_type='application/rss+xml',
    )


class GenrePodcastFeed(RecordingsPodcastFeed):
    artwork_link = static('artwork.png')

    def get_object(self, request, genre_id):
        return Genre.objects.get(id=genre_id)

    def link(self, obj):
        return obj.web_url

    def title(self, obj):
        return 'Boiler Room - %s' % obj.title

    def subtitle(self, obj):
        return obj.description

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return obj.recordings.all()
