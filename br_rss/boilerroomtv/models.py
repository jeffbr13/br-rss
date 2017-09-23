from django.db import models


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

    class Meta:
        ordering = ('-released',)

    def __str__(self):
        return self.title
