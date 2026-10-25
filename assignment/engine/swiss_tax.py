from decimal import ROUND_HALF_UP, Decimal

from assignment.engine.swiss_social_security import swiss_social_security
from assignment.rules import SWISS_TAX as RULES


def tax_on_slices(income, slices):
    tax = Decimal(0)
    for width, rate in slices:
        part = min(income, width)
        tax += part * rate
        income -= part
    return tax


def cut_to_hundreds(income):
    return income // 100 * 100


def to_francs(amount):
    return amount.quantize(Decimal(1), rounding=ROUND_HALF_UP)


def federal_tax(taxable_income):
    income = cut_to_hundreds(taxable_income)
    if income >= RULES["federal_flat_from"]:
        return income * RULES["federal_flat_rate"]
    return tax_on_slices(income, RULES["federal_slices"])


def zurich_simple_tax(taxable_income):
    return tax_on_slices(cut_to_hundreds(taxable_income), RULES["zurich_slices"])


def swiss_income_tax(gross_pay, pension=Decimal(0)):
    """Income tax of a single person in the city of Zurich, without church tax.

    Takes off the employee social security, the pension and accident insurance
    contributions, the work costs and the insurance deduction. The federal tax
    and the canton and city tax are then worked out on their own income.
    """
    net_pay = gross_pay - swiss_social_security(gross_pay)["total"] - pension
    work_costs = net_pay * RULES["work_costs_rate"]
    work_costs = max(RULES["work_costs_min"], min(RULES["work_costs_max"], work_costs))

    if pension > 0:
        insurance = RULES["insurance_deduction_with_pension"]
    else:
        insurance = RULES["insurance_deduction_without_pension"]

    taxable_federal = net_pay - work_costs - insurance["federal"]
    taxable_canton = net_pay - work_costs - insurance["canton"]
    simple_tax = zurich_simple_tax(taxable_canton)

    federal = to_francs(federal_tax(taxable_federal))
    canton = to_francs(simple_tax * RULES["canton_multiplier"])
    city = to_francs(simple_tax * RULES["city_multiplier"])
    return {
        "taxable_federal": taxable_federal,
        "taxable_canton": taxable_canton,
        "federal": federal,
        "canton": canton,
        "city": city,
        "total": federal + canton + city,
    }
