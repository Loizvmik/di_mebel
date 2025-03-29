from django.db import models


class Vacancy(models.Model):
    work = models.CharField(max_length=255)

    def __str__(self):
        return self.work


class VacancyPerson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=20, unique=True)
    vacancyId = models.OneToOneField(Vacancy, on_delete=models.CASCADE, related_name="form")

    def __str__(self):
        return self.name
