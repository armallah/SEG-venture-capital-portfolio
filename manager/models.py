import datetime
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from pandas._libs.tslibs.parsing import parse_datetime_string

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'viewer'),
        (2, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES)

    def full_name(self):
        return (self.first_name + " " + self.last_name) #Get string with name and surname

    pass

class Entity(models.Model):
    name = models.CharField(max_length=50)

    ## The following is made only to appease the type checker (No special stuff here)
    invested_company: models.QuerySet["Company"]
    founding_company: models.QuerySet["Company"]
    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getTotalFoundedCompanies(self):
        return self.founding_company.count()

    def getTotalInvestedCompanies(self):
        return self.invested_company.count()

class Company(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, blank=False, null=False)
    country_code = models.CharField(max_length=15)
    wayra_investment = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    description = models.CharField(max_length=200, blank=True, null=True)
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
    rounds = models.QuerySet["Round"]

    def update_comp(self, new_info: dict):
        self.name = new_info['Company']
        self.country_code = new_info['Hub']
        self.description = new_info['Description (ENG)']
        self.wayra_investment = new_info['Wayra Total Investment (ML)']
        self.save()

    def isPortfolio(self):
        return self.wayra_investment != 0

    def __str__(self):
        return self.name

    def getTotalInvestors(self):
        return self.investors.count()

    def getTotalFounders(self):
        return self.founders.count()

    def getTotalRounds(self):
        return self.rounds.count()

    def getTotalRights(self):
        return self.wayra_right.count()


class Investing(models.Model):
    investor = models.ForeignKey(Entity, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits = 20, decimal_places=3)

    def get_amount(self):
        return self.amount

class Round(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="rounds")
    round_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    equity = models.DecimalField(max_digits=20, decimal_places=3, validators = [MinValueValidator(0)], default=0)
    wayra_equity=models.DecimalField(max_digits=20, decimal_places=3, validators = [MinValueValidator(0)], default=0)

    pre_money_valuation = models.DecimalField(max_digits=20, decimal_places=3, validators = [MinValueValidator(0)], default=0)

    round_date = models.DateField(null=True)
    def update_round(self, new_info: dict):
        self.equity = new_info.get(f"(Round {self.round_number}) - Investors Equity") or 0
        self.wayra_equity = new_info.get(f"(Round {self.round_number}) - Wayra Follow-on") or 0
        date_str:str = new_info.get(f"(Round {self.round_number}) - Date Link") or ""
        self.round_date = parse_datetime_string(date_str, dayfirst=True, yearfirst=False)
        self.pre_money_valuation = new_info.get(f"(Round {self.round_number}) - Pre-money valuation") or 0
        self.save()

    def __str__(self) -> str:
        return f"{self.company.name} Round:{self.round_number}"

class Right(models.Model):
    name = models.CharField(max_length=50)
    holding_right = models.ManyToManyField(Company, related_name="wayra_right")

class Document(models.Model):
    upload = models.FileField(upload_to='documents/')

#     @property
#     def file_url(self):
#         if self.file and hasattr(self.file, 'url'):
#             return self.file.path
