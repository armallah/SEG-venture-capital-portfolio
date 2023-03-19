import datetime
from django.test import TestCase
from manager.utils import airtable
from manager.models import Company, Round
class LogInViewTestCase(TestCase):

    def setUp(self):
        airtable.update_all()


    def testItem(self):
        pixelpin :Company = Company.objects.filter(number = "W00264").first() \
                or self.fail("company number W00264 do not exist")
        self.assertEqual(pixelpin.name, "Pixel Pin")
        self.assertEqual(pixelpin.country_code, "UK")
        self.assertEqual(pixelpin.description, "Replacing passwords with pictures")
        self.assertEqual(pixelpin.wayra_investment, 50000)

    def testRound(self):
        self.assertNotEqual(Round.objects.all(), None)
        round1 :Round = Round.objects.filter(company__number="W00264", round_number=1).first()\
                or self.fail("round 1 of company number W00264 do not exist")
        round2 :Round = Round.objects.filter(company__number="W00264", round_number=2).first()\
                or self.fail("round 2 of company number W00264 do not exist")
        self.assertEqual(round1.company.name, "Pixel Pin")
        self.assertEqual(round1.equity, 0)
        self.assertEqual(round1.wayra_equity, 0)
        self.assertEqual(round1.pre_money_valuation, 0)
        self.assertEqual(round1.round_date, datetime.date(2012, 6, 1)) 
        self.assertEqual(round2.company.name, "Pixel Pin")
        self.assertEqual(round2.equity, 150000)
        self.assertEqual(round2.wayra_equity, 0)
        self.assertEqual(round2.pre_money_valuation, 1350000)
        
        round2b :Round = Round.objects.filter(company__number="W00272", round_number=2).first()\
                or self.fail("round 2 of company number W00272 do not exist")
        self.assertEqual(round2b.company.name, "Base Stone (Blue Ronin)")
        self.assertEqual(round2b.equity, 674995)
        self.assertEqual(round2b.wayra_equity, 0)
        self.assertEqual(round2b.pre_money_valuation, 6924680)
