from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify

def profile_image_path(instance, filename):
    return f"profile_image/{instance.user.id}.png"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_list_public = models.BooleanField(default=True)
    is_cover_in_list = models.BooleanField(default=True)

    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Media(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)

    type = models.ForeignKey('Type', models.PROTECT, null=True)
    status = models.ForeignKey('Status', models.PROTECT, null=True)

    rating = models.FloatField(default=7.0)
    number_of_ratings = models.IntegerField(default=1)

    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)

    number_of_seasons = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_series = models.PositiveSmallIntegerField(blank=True, null=True)

    genres = models.ManyToManyField('Genre', blank=True)

    studios = models.ManyToManyField('Studio', blank=True)
    cover = models.ImageField(upload_to="covers", blank=True, null=True)

    is_published = models.BooleanField(default=True, null=True)

    def __str__(self):
        return f"{self.title} / {self.id}"
    
    def get_absolute_url(self):
        return f'/{settings.MEDIA_ENTITY_SLUG}/{self.id}/{slugify(self.title)}'

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'
        ordering = ["-rating"]


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{settings.MEDIA_COLLECTION_SLUG}/?genres={self.name}'

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ["name"]


class Status(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        ordering = ["name"]


class Type(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'


class Studio(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{settings.MEDIA_COLLECTION_SLUG}/?studios={self.name}'

    class Meta:
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'
