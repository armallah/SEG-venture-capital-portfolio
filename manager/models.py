from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'viewer'),
        (2, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES)
    pass

class Entity(models.Model):
    name = models.CharField(max_length=50)
    
    ## The following is made only to appease the type checker (No special stuff here)
    invested_company: models.QuerySet["Company"]
    founding_company: models.QuerySet["Company"]
    def getName(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, blank=False, null=False)
    country_code = models.CharField(max_length=15)
    wayra_investment = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    investors = models.ManyToManyField(
            Entity,
            through='Investing',
            through_fields=('company','investor'),
            related_name='invested_company'
        )
    founders = models.ManyToManyField(
            Entity,
            related_name='founding_company'
            )
    wayra_right: models.QuerySet["Right"]

    def isPortfolio(self):
        return self.wayra_investment != 0

    def __str__(self):
        return self.number + str(self.founders)



class Investing(models.Model):
    investor = models.ForeignKey(Entity, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits = 20, decimal_places=3)

    def __str__(self):
        return self.name


class Right(models.Model):
    name = models.CharField(max_length=50)
    holding_right = models.ManyToManyField(Company, related_name="wayra_right")

class Document(models.Model):
    upload = models.FileField(upload_to='documents/')

    @property
    def file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.path

