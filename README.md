# LibraryAPI_Diplom
celery -A config worker -P eventlet -l info
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
