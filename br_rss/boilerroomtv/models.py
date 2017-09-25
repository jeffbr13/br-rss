from django.db import models
from django.urls import reverse


class Genre(models.Model):
    url = models.URLField(unique=True)
    web_url = models.URLField(unique=True)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre-rss', kwargs=dict(genre_id=self.id))


class Recording(models.Model):
    url = models.URLField(unique=True)
    web_url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    artists = models.CharField(max_length=300)
    released = models.DateTimeField()
    duration = models.DurationField()
    thumbnail_url = models.URLField(blank=True)
    audio_url = models.URLField()
    audio_content_type = models.CharField(max_length=200)
    audio_content_length = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name='recordings')

    class Meta:
        ordering = ('-released',)

    def __str__(self):
        return self.title


class Channel(models.Model):
    url = models.URLField(unique=True)
    web_url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=200, blank=True)
    thumbnail_url = models.URLField()
    featured_recordings = models.ManyToManyField(Recording, related_name='featured_in_channels')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('channel-rss', kwargs=dict(channel_id=self.id))
