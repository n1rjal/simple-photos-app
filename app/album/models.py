from django.contrib.auth.models import User
from django.db import models

from photo.models import Photo
from core.abstract_models import TimeStampedModel


# Create your models here.
class Album(TimeStampedModel):
    owner = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_query_name="albums",
    )
    name = models.CharField(max_length=250, blank=False, null=False)
    access_users = models.ManyToManyField(
        User,
        related_name="shared_albums",
    )
    photos = models.ManyToManyField(Photo, related_name="albums")

    def __str__(self):
        return self.name
