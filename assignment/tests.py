from decimal import Decimal

from django.test import SimpleTestCase

from assignment.engine.gross_up import gross_up
from assignment.engine.swiss_social_security import swiss_social_security
from assignment.engine.swiss_tax import federal_tax, swiss_income_tax
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


class GrossUpTests(SimpleTestCase):
    def test_tax_equals_tax_on_income_plus_tax(self):
        for income in [20000, 60000, 80000, 110000, 158868, 250000]:
            income = Decimal(income)
            tax, rounds = gross_up(income)
            self.assertAlmostEqual(tax, uk_tax(income + tax), places=2)

    def test_one_step_answer_is_too_low_when_the_allowance_is_lost(self):
        income = Decimal(110000)
        tax, rounds = gross_up(income)
        one_step = uk_tax(income) / (1 - Decimal("0.4"))
        self.assertGreater(tax, one_step + 5000)
        self.assertAlmostEqual(tax, Decimal("64914.545"), places=2)


class SwissSocialSecurityTests(SimpleTestCase):
    def test_one_side_on_170000(self):
        social = swiss_social_security(Decimal(170000))
        self.assertEqual(social["ahv_iv_eo"], 9010)
        self.assertEqual(social["alv"], Decimal("1630.2"))
        self.assertEqual(social["total"], Decimal("10640.2"))

    def test_unemployment_insurance_stops_at_the_limit(self):
        at_limit = swiss_social_security(Decimal(148200))
        far_above = swiss_social_security(Decimal(300000))
        self.assertEqual(at_limit["alv"], far_above["alv"])


class SwissTaxTests(SimpleTestCase):
    def test_federal_tariff_matches_the_estv_example(self):
        tax = federal_tax(Decimal(60000))
        self.assertAlmostEqual(tax, Decimal("671.40"), delta=Decimal("0.05"))

    def test_170000_without_pension(self):
        tax = swiss_income_tax(Decimal(170000))
        self.assertEqual(tax["federal"], 7362)
        self.assertEqual(tax["canton"], 10673)
        self.assertEqual(tax["city"], 13370)
        self.assertEqual(tax["total"], 31405)

    def test_170000_matches_the_official_calculator_with_its_pension(self):
        tax = swiss_income_tax(Decimal(170000), Decimal(5988 + 593))
        self.assertEqual(tax["federal"], 6735)
        self.assertEqual(tax["canton"], 10130)
        self.assertEqual(tax["city"], 12689)
