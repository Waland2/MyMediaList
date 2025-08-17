from django.db import models
from main.models import Media, User

class MyListStatus(models.Model):
    name = models.CharField(max_length=50)
    priority_in_list = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
    
class MyListScores(models.Model):
    value = models.SmallIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"({self.value}) {self.name}"

    class Meta:
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'


class MyListObject(models.Model):
    media_item = models.ForeignKey(Media, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    watch_status = models.ForeignKey(MyListStatus, on_delete=models.CASCADE, default=1)
    score = models.ForeignKey(MyListScores, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=750, blank=True)    

    class Meta:
        verbose_name = 'List Object'
        verbose_name_plural = 'List Objects'
