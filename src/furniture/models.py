from django.db import models

class Furniture(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    characteristic = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255)

class Image(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=255, null=True,blank=True)
    furniture_id = models.ForeignKey(
        Furniture,
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True)

