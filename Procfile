web: python br_rss/manage.py collectstatic --noinput; python br_rss/manage.py migrate --noinput; gunicorn --chdir=br_rss --bind=0.0.0.0:$PORT br_rss.wsgi:application
worker: python -u br_rss/manage.py run_huey
