from decimal import Decimal

from assignment.rules import UK_INCOME_TAX as RULES


def uk_tax(income):
    """UK income tax for one tax year.

    The personal allowance goes down by 1 for every 2 of income above 100,000
    and is gone at 125,140. The rest is taxed in three bands.
    """
    allowance = RULES["personal_allowance"]
    allowance -= max(Decimal(0), (income - RULES["taper_starts"]) / 2)
    allowance = max(Decimal(0), allowance)

    taxable = max(Decimal(0), income - allowance)
    basic = min(taxable, RULES["basic_rate_limit"])
    higher = min(taxable, RULES["higher_rate_limit"]) - basic
    additional = taxable - basic - higher

    return (
        basic * RULES["basic_rate"]
        + higher * RULES["higher_rate"]
        + additional * RULES["additional_rate"]
    )
