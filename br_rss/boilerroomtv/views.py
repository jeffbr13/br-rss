from django.http import HttpRequest
from django.shortcuts import render

from .models import Recording


def index(request: HttpRequest):
    return render(request, 'index.html')


def podcast_feed(request: HttpRequest):
    return render(
        request,
        'rss.xml',
        context=dict(
            server_url='%s/%s' % (request._get_scheme(), request.get_host()),
            podcasts=Recording.objects.all(),
        ),
        content_type='application/rss+xml',
    )
