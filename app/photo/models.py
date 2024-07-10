from django.db import models
from django.contrib.auth.models import User

from core.abstract_models import TimeStampedModel


class Photo(TimeStampedModel):
    url = models.URLField(
        max_length=250,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    owner = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    access_users = models.ManyToManyField(
        to=User,
        related_query_name="shared_photos",
    )

    def __str__(self) -> str:
        return self.name


class PhotoMetaData(models.Model):
    capture_time = models.DateTimeField(blank=False, null=False)
    photo = models.OneToOneField(
        to=Photo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="metadata",
    )

    def __str__(self):
        return str(self.photo)
