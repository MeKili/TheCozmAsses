from decimal import Decimal

from assignment.engine.benefits import benefit_rows
from assignment.engine.gross_up import gross_up
from assignment.engine.social_security_rule import social_security_rule
from assignment.engine.swiss_social_security import swiss_social_security
from assignment.engine.swiss_tax import swiss_income_tax
from assignment.engine.uk_tax import uk_tax
from assignment.rules import (
    SWISS_SOCIAL_SECURITY,
    SWISS_TAX,
    UK_EMPLOYER_NI,
    UK_GROSS_UP,
    UK_INCOME_TAX,
)


def row(label, values, sources=(), tag="", note=""):
    return {"label": label, "values": values, "sources": sources, "tag": tag, "note": note}


def section(title, rows, years):
    totals = [sum(r["values"][year] for r in rows) for year in range(years)]
    return {"title": title, "rows": rows, "totals": totals}


def cost_table(inputs):
    """Works out what the assignment costs the employer in every year, in pounds.

    The pay at home is paid in francs and the benefits in pounds or francs. The
    employee gets the net home pay, the employer pays the UK tax on it and on
    the benefits, and keeps the Swiss tax and social security it takes off.
    """
    rule = social_security_rule(
        inputs["start"], inputs["end"], inputs["replaces_another_worker"]
    )
    uk_rule = rule["country"] == "United Kingdom"
    years = rule["months"] // 12
    rate = inputs["exchange_rate"]
    swiss_pay = inputs["salary"] + inputs["bonus"]

    swiss_tax = swiss_income_tax(swiss_pay, inputs["pension"])
    one_side = swiss_social_security(swiss_pay)["total"]
    net_home_pay = (swiss_pay - swiss_tax["total"] - one_side) / rate

    benefits = benefit_rows(inputs["benefits"], years, rate, inputs["flights"])

    income_tax, tax_on_tax, employer_ni, class_1a, working = [], [], [], [], []
    for year in range(years):
        taxable_cash = sum(b["taxable"][year] for b in benefits if b["taxable_is_cash"])
        taxable_in_kind = sum(
            b["taxable"][year] for b in benefits if not b["taxable_is_cash"]
        )
        income = net_home_pay + taxable_cash + taxable_in_kind
        tax, rounds = gross_up(income)

        income_tax.append(uk_tax(income))
        tax_on_tax.append(tax - uk_tax(income))
        working.append({"year": year + 1, "income": income, "tax": tax, "rounds": rounds})

        employer_ni.append(Decimal(0))
        class_1a.append(Decimal(0))
        if uk_rule:
            cash_pay = net_home_pay + taxable_cash + tax
            above_threshold = max(Decimal(0), cash_pay - UK_EMPLOYER_NI["secondary_threshold"])
            employer_ni[year] = above_threshold * UK_EMPLOYER_NI["employer_rate"]
            class_1a[year] = taxable_in_kind * UK_EMPLOYER_NI["class_1a_rate"]

    home_pay = section(
        "Home pay",
        [
            row("Base salary", [inputs["salary"] / rate] * years),
            row("Bonus", [inputs["bonus"] / rate] * years),
        ],
        years,
    )

    assignment_benefits = section(
        "Assignment benefits",
        [row(b["name"], b["cost"], b["sources"], b["tag"], b["note"]) for b in benefits],
        years,
    )

    host_rows = [
        row(
            "UK income tax on the pay and the taxable benefits",
            income_tax,
            UK_INCOME_TAX["sources"],
        ),
        row(
            "Tax on the tax (the tax the employer pays is taxable too)",
            tax_on_tax,
            UK_GROSS_UP["sources"],
        ),
    ]
    if uk_rule:
        host_rows.append(
            row("UK employer National Insurance (Class 1)", employer_ni, UK_EMPLOYER_NI["sources"])
        )
        host_rows.append(
            row(
                "UK employer National Insurance on benefits (Class 1A)",
                class_1a,
                UK_EMPLOYER_NI["sources"],
            )
        )
    else:
        paid = [one_side / rate] * years
        host_rows.append(
            row("Swiss social security paid, employer share", paid, SWISS_SOCIAL_SECURITY["sources"])
        )
        host_rows.append(
            row(
                "Swiss social security paid, employee share",
                paid,
                SWISS_SOCIAL_SECURITY["sources"],
                note="Taken off the pay and paid to the Swiss fund.",
            )
        )
    host_charges = section("Host tax and charges paid by the employer", host_rows, years)

    deductions = section(
        "Deductions",
        [
            row(
                "Hypothetical Swiss income tax",
                [-swiss_tax["total"] / rate] * years,
                SWISS_TAX["sources"],
                note=(
                    f"Federal {swiss_tax['federal']:,.0f}, canton {swiss_tax['canton']:,.0f}, "
                    f"city {swiss_tax['city']:,.0f} (francs a year)."
                ),
            ),
            row(
                "Hypothetical Swiss social security",
                [-one_side / rate] * years,
                SWISS_SOCIAL_SECURITY["sources"],
            ),
        ],
        years,
    )

    sections = [home_pay, assignment_benefits, host_charges, deductions]
    total_cost = [sum(s["totals"][year] for s in sections) for year in range(years)]
    overall_total = sum(total_cost)

    return {
        "years": years,
        "exchange_rate": rate,
        "rule": rule,
        "sections": sections,
        "total_cost": total_cost,
        "overall_total": overall_total,
        "overall_total_chf": overall_total * rate,
        "multiple_by_year": [t / h for t, h in zip(total_cost, home_pay["totals"])],
        "multiple": overall_total / sum(home_pay["totals"]),
        "working": working,
    }
