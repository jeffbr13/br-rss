web: cd br_rss; python manage.py collectstatic --noinput; python manage.py migrate --noinput; waitress-serve --port=$PORT br_rss.wsgi:application
worker: python -u br_rss/manage.py run_huey
