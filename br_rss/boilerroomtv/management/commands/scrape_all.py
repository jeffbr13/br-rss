from django.core.management.base import BaseCommand

from ...tasks import scrape_genres, scrape_all_recordings, scrape_channels


class Command(BaseCommand):
    def handle(self, *args, **options):
        scrape_genres()
        scrape_all_recordings()
        scrape_channels()
