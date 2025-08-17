import time
from django.db import models
from main.models import Media, Genre, Status, Type, Studio, User

def cover_upload_path(instance, filename):
    return f"covers/{instance.pk or 'temp'}_{int(time.time())}.jpg"

class TempMedia(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    type_of_request = models.CharField(choices=[('add', 'Add'), ('edit', 'Edit')], max_length=4, default='edit')
    media_item = models.ForeignKey(Media, models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    type = models.ForeignKey(Type, models.PROTECT, null=True)
    status = models.ForeignKey(Status, models.PROTECT, null=True)

    rating = models.FloatField(default=7.0)
    number_of_ratings = models.IntegerField(default=1)

    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)

    number_of_seasons = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_series = models.PositiveSmallIntegerField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, blank=True)

    studios = models.ManyToManyField(Studio, blank=True)
    cover = models.ImageField(upload_to=cover_upload_path, blank=True, null=True)

    is_published = models.BooleanField(default=True, null=True)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
        # ordering = ["-rating"]

