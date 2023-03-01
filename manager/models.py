from django.db import models
# Create your models here.

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


class Users(AbstractUser): # user class
    first_name = models.CharField(max_length=30, help_text='Enter firstname')
    last_name = models.CharField(max_length=30, help_text='Enter lastname')
    username = models.EmailField(max_length = 50, unique = True, help_text = 'Enter a unique email')
    #email = models.EmailField(max_length=255, unique=True, help_text='Enter email')
    USER_TYPE_CHOICES = ((1, 'Portfolio manager'),(2, 'Admin'))
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES , default=1)

    def full_name(self):
        return (self.first_name + " " + self.last_name)



class Investing(models.Model):
    investor = models.ForeignKey(Entity, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits = 20, decimal_places=3)

class Right(models.Model):
    name = models.CharField(max_length=50)
    holding_right = models.ManyToManyField(Company, related_name="wayra_right")
    
