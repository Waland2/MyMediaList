from main.models import Media
from mymedialist.celery import app
from .models import MyListObject


@app.task
def calculate_ratings():
    media = list(Media.objects.all())
    for media_item in media:
        ml_objects = MyListObject.objects.filter(media_item=media_item)

        # by default all media items have rating 7 with 1 review
        score = 7
        scores_count = len(ml_objects) + 1

        for obj in ml_objects:
            if obj.score:
                score += obj.score.value
        
        final_score = score / max(scores_count, 1)

        media_item.rating = final_score
        media_item.number_of_ratings = scores_count
        media_item.save()


    MyListObject.objects.all()