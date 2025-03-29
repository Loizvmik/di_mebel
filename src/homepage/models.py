from django.db import models
from src.furniture.models import Image

class Team(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.OneToOneField(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team'
    )
    def __str__(self):
        return self.name