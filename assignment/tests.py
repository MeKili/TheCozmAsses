from datetime import date
from decimal import Decimal
from urllib.parse import urlparse

from django.test import SimpleTestCase

from assignment import rules
from assignment.engine.benefits import benefit_rows
from assignment.engine.cost_table import cost_table
from assignment.engine.gross_up import gross_up
from assignment.engine.immigration import immigration_costs, immigration_steps
from assignment.engine.social_security_rule import social_security_rule
from assignment.engine.swiss_social_security import swiss_social_security
from assignment.engine.swiss_tax import federal_tax, swiss_income_tax
from assignment.engine.uk_tax import uk_tax
from assignment.forms import CostForm, flatten
from assignment.test_case import TEST_CASE


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


class SocialSecurityRuleTests(SimpleTestCase):
    def test_exactly_24_months_stays_swiss(self):
        rule = social_security_rule(date(2026, 4, 6), date(2028, 4, 5), False)
        self.assertEqual(rule["country"], "Switzerland")
        self.assertEqual(rule["months"], 24)

    def test_more_than_24_months_flips_to_the_uk(self):
        one_day_more = social_security_rule(date(2026, 4, 6), date(2028, 4, 6), False)
        one_month_more = social_security_rule(date(2026, 4, 6), date(2028, 5, 5), False)
        self.assertEqual(one_day_more["country"], "United Kingdom")
        self.assertEqual(one_month_more["country"], "United Kingdom")
        self.assertEqual(one_month_more["months"], 25)

    def test_replacing_another_worker_flips_to_the_uk(self):
        rule = social_security_rule(date(2026, 4, 6), date(2028, 4, 5), True)
        self.assertEqual(rule["country"], "United Kingdom")


class BenefitsTests(SimpleTestCase):
    moving = {
        "name": "Moving costs", "type": "moving", "amount": Decimal(6000),
        "currency": "GBP", "paid": "once in year 1",
    }
    temporary_housing = {
        "name": "Temporary housing", "type": "temporary_housing", "amount": Decimal(4000),
        "currency": "GBP", "paid": "once in year 1",
    }

    def test_removal_costs_over_the_limit_are_taxable(self):
        rows = benefit_rows([self.moving, self.temporary_housing], 2, Decimal("1.10"), Decimal(0))
        self.assertEqual(sum(row["taxable"][0] for row in rows), 2000)
        self.assertEqual(rows[0]["tag"], "not taxable in the UK")
        self.assertEqual(rows[1]["tag"], "part taxable benefit in kind")

    def test_flights_do_not_use_up_the_limit(self):
        rows = benefit_rows([self.moving, self.temporary_housing], 2, Decimal("1.10"), Decimal(1500))
        self.assertEqual(sum(row["taxable"][0] for row in rows), 500)


class CostTableTests(SimpleTestCase):
    def test_pack_test_case_gives_a_table_for_both_years(self):
        table = cost_table(TEST_CASE)
        self.assertEqual(table["years"], 2)
        self.assertEqual(table["rule"]["country"], "Switzerland")
        self.assertEqual([s["title"] for s in table["sections"]], [
            "Home pay",
            "Assignment benefits",
            "Host tax and charges paid by the employer",
            "Deductions",
        ])
        self.assertAlmostEqual(table["total_cost"][0], Decimal("291111.27"), delta=Decimal("0.01"))
        self.assertAlmostEqual(table["total_cost"][1], Decimal("271210.45"), delta=Decimal("0.01"))

    def test_rows_add_up_to_the_total_and_the_grossed_up_tax(self):
        table = cost_table(TEST_CASE)
        rows = [r for s in table["sections"] for r in s["rows"]]
        for year in range(2):
            self.assertEqual(sum(r["values"][year] for r in rows), table["total_cost"][year])
            host_rows = table["sections"][2]["rows"]
            uk_tax_paid = host_rows[0]["values"][year] + host_rows[1]["values"][year]
            self.assertEqual(uk_tax_paid, table["working"][year]["tax"])


class FormTests(SimpleTestCase):
    def test_pack_test_case_is_accepted_as_given(self):
        form = CostForm(flatten(TEST_CASE))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(len(form.cleaned_data["benefits"]), 4)

    def test_bad_input_gives_readable_messages(self):
        data = flatten(TEST_CASE)
        data["salary"] = ""
        data["bonus"] = "-5"
        data["exchange_rate"] = "0"
        form = CostForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["salary"], ["This field is required."])
        self.assertIn("greater than or equal to 0", form.errors["bonus"][0])
        self.assertEqual(form.errors["exchange_rate"], ["The exchange rate must be more than 0."])

    def test_dates_must_be_in_order_and_whole_years(self):
        data = flatten(TEST_CASE)
        data["end"] = "2026-03-01"
        self.assertIn("must be after the start date", CostForm(data).errors["end"][0])
        data["end"] = "2028-05-05"
        self.assertIn("whole number of years", CostForm(data).errors["end"][0])


class SourceTests(SimpleTestCase):
    official_sites = ["gov.uk", "admin.ch", "zh.ch", "stadt-zuerich.ch", "ahv-iv.ch"]

    def find_urls(self, value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "url":
                    yield item
                else:
                    yield from self.find_urls(item)
        elif isinstance(value, list):
            for item in value:
                yield from self.find_urls(item)

    def test_every_source_link_is_on_an_official_site(self):
        everything = [getattr(rules, name) for name in dir(rules) if name.isupper()]
        urls = list(self.find_urls(everything))
        self.assertGreater(len(urls), 20)
        for url in urls:
            host = urlparse(url).hostname
            official = any(host == site or host.endswith("." + site) for site in self.official_sites)
            self.assertTrue(official, url)


class ImmigrationTests(SimpleTestCase):
    def test_work_permit_business_visit_and_passport_each_have_an_answer_and_sources(self):
        titles = [card["title"] for card in rules.IMMIGRATION_CARDS]
        self.assertIn("Work permit", titles)
        self.assertTrue(any(title.startswith("Business visit") for title in titles))
        self.assertIn("Passport", titles)
        for card in rules.IMMIGRATION_CARDS:
            for point in card["points"]:
                self.assertTrue(point["sources"], point["text"])

    def test_costs_for_two_years(self):
        without_licence = immigration_costs(2, "large", True, "standard")
        self.assertEqual(without_licence["total"], 819 + 2070 + 525 + 2640)
        with_licence = immigration_costs(2, "large", False, "standard")
        self.assertEqual(with_licence["total"], without_licence["total"] + 1682)

    def test_visa_fee_is_higher_for_stays_over_three_years(self):
        self.assertEqual(immigration_costs(3, "small", True, "standard")["lines"][0]["amount"], 819)
        self.assertEqual(immigration_costs(4, "small", True, "standard")["lines"][0]["amount"], 1618)

    def test_weeks_add_the_licence_and_the_decision(self):
        self.assertEqual(immigration_steps(True, "standard")["weeks"], 3)
        self.assertEqual(immigration_steps(False, "standard")["weeks"], 11)


class PageTests(SimpleTestCase):
    def test_cost_page_shows_the_table_for_the_test_case(self):
        page = self.client.get("/?test_case=1").content.decode()
        self.assertIn("291,111.27", page)
        self.assertIn("271,210.45", page)

    def test_immigration_page_states_a_requirement_for_all_three(self):
        page = self.client.get("/immigration/").content.decode()
        self.assertIn("Work permit", page)
        self.assertIn("Business visit before the assignment", page)
        self.assertIn("Passport", page)
        self.assertIn("https://www.gov.uk/senior-specialist-worker-visa", page)

    def test_immigration_page_survives_bad_input(self):
        response = self.client.get("/immigration/?years=9&speed=fast")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ensure this value is less than or equal to 5", response.content.decode())
