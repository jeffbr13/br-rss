"""br_rss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from boilerroomtv.views import index, AllRecordingsPodcastFeed, ChannelPodcastFeed, GenrePodcastFeed

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^rss/$', AllRecordingsPodcastFeed(), name='rss'),
    url(r'^rss/channels/(?P<channel_id>[0-4])/$', ChannelPodcastFeed(), name='channel-rss'),
    url(r'^rss/genres/(?P<genre_id>\d+)/$', GenrePodcastFeed(), name='genre-rss'),
]
