from manager.models import Company, Investing, Round, Right
from manager.utils import airtable

class Command(BaseCommand):
    def __init__(self):
        pass
    def handle(self, *args, **options):
        airtable.update_all()
