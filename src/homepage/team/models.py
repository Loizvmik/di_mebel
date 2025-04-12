from django.db import models
from src.furniture.models import Image


class Team(models.Model):
    image = models.OneToOneField(
        Image,
        on_delete=models.SET_NULL,
        related_name='team',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name