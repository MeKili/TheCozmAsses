from decimal import Decimal

from django.test import SimpleTestCase

from assignment.engine.uk_tax import uk_tax


class UkTaxTests(SimpleTestCase):
    def test_band_edges(self):
        self.assertEqual(uk_tax(Decimal(12570)), 0)
        self.assertEqual(uk_tax(Decimal(50270)), 7540)
        self.assertEqual(uk_tax(Decimal(100000)), 27432)
        self.assertEqual(uk_tax(Decimal(125140)), 42516)
        self.assertEqual(uk_tax(Decimal(200000)), 76203)

    def test_lost_allowance_makes_the_rate_60_percent(self):
        extra_tax = uk_tax(Decimal(110000)) - uk_tax(Decimal(100000))
        self.assertEqual(extra_tax, 6000)
