# mymedialist

# Launch
```
1) pip install -r requirements.txt
2) edit mymedialist/settings.py
3) python manage.py migrate
4) celery -A mymedialist worker -l info
5) celery -A mymedialist beat -l info
6) python manage.py runserver
```

docker exec -it mml_django python manage.py loaddata fixtures/main.json