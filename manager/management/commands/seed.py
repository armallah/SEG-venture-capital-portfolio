from manager.models import Company, Entity, Investing, Round, Right

class Command(BaseCommand):
    def __init__(self):
        pass
    def handle(self, *args, **options):
        Company.objects.create(name = "Pixel Pin", number = "W00264", country_code = "Reino Unido", wayra_investment = 50000.00)
        Company.objects.create(name = "Base Stone", number = "W00272", country_code = "Reino Unido", wayra_investment = 51006.00)
        Company.objects.create(name = "Eventstagram", number = "W00278", country_code = "Reino Unido", wayra_investment = 51006.00)
        Company.objects.create(name = "Narrato", number = "W00284", country_code = "Reino Unido", wayra_investment = 76006.00)
        