from assignment.rules import (
    CERTIFICATES,
    FASTER_DECISION,
    IMMIGRATION_COSTS as COSTS,
    SKILLS_CHARGE,
    SPONSOR_LICENCE,
    SSW_COSTS,
    SSW_OVERVIEW,
    SWISS_CERTIFICATE,
)


def cost_line(label, amount, paid_by, sources, note=""):
    return {"label": label, "amount": amount, "paid_by": paid_by, "sources": sources, "note": note}


def immigration_costs(years, company_size, has_licence, speed):
    """What the work visa costs for a stay of some years, in pounds.

    The employee pays the visa fee and the health surcharge. The UK company
    pays the certificate, the skills charge and the sponsor licence.
    """
    if years <= 3:
        visa_fee = COSTS["visa_fee_up_to_3_years"]
    else:
        visa_fee = COSTS["visa_fee_over_3_years"]

    extra_half_years = 2 * (years - 1)
    skills_charge = (
        COSTS["skills_charge_first_12_months"][company_size]
        + extra_half_years * COSTS["skills_charge_each_extra_6_months"][company_size]
    )

    lines = [
        cost_line("Visa application fee", visa_fee, "The employee", [SSW_COSTS]),
        cost_line(
            "Immigration health surcharge",
            years * COSTS["health_surcharge_per_year"],
            "The employee",
            [SSW_COSTS],
            note="For each year of the stay.",
        ),
        cost_line(
            "Certificate of sponsorship",
            COSTS["certificate_of_sponsorship"],
            "The UK company",
            [CERTIFICATES],
        ),
        cost_line(
            "Immigration skills charge",
            skills_charge,
            "The UK company",
            [SKILLS_CHARGE],
            note="For the first 12 months and each extra 6 months of the stay.",
        ),
    ]
    if not has_licence:
        lines.append(
            cost_line(
                "Sponsor licence",
                COSTS["sponsor_licence"][company_size],
                "The UK company",
                [SPONSOR_LICENCE],
            )
        )
    if speed != "standard":
        lines.append(
            cost_line(
                f"Faster decision ({speed} service)",
                COSTS["faster_decision"][speed],
                "The employee",
                [FASTER_DECISION],
            )
        )

    return {
        "lines": lines,
        "total": sum(line["amount"] for line in lines),
        "employee_total": sum(l["amount"] for l in lines if l["paid_by"] == "The employee"),
        "company_total": sum(l["amount"] for l in lines if l["paid_by"] == "The UK company"),
    }


def immigration_steps(has_licence, speed):
    """The steps to get the work visa, with how long each takes.

    The weeks only add up the decisions of the sponsor licence and the visa.
    Time to get documents and appointments comes on top.
    """
    weeks = COSTS["weeks_for_decision"][speed]
    steps = []
    if not has_licence:
        weeks += COSTS["weeks_for_licence"]
        steps.append(
            {
                "what": "The UK company gets a sponsor licence",
                "time": "Usually less than 8 weeks. For 750 pounds more, a decision within 10 working days.",
                "sources": [SPONSOR_LICENCE],
            }
        )

    decision_times = {
        "standard": "Usually within 3 weeks, when the employee applies from outside the UK.",
        "priority": "About 5 working days with the priority service.",
        "super priority": "By the end of the next working day with the super priority service.",
    }
    steps += [
        {
            "what": "The UK company assigns the certificate of sponsorship",
            "time": "From the certificates it got with its licence. Extra certificates usually take up "
            "to 12 weeks, or 5 working days for a fee.",
            "sources": [CERTIFICATES],
        },
        {
            "what": "The Swiss employer asks for the certificate of coverage",
            "time": "Ask before the assignment starts, then keep it.",
            "sources": [SWISS_CERTIFICATE],
        },
        {
            "what": "The employee applies online, proves identity and gives documents",
            "time": "Up to 3 months before the start date. Allow extra time if an appointment is needed.",
            "sources": [SSW_OVERVIEW],
        },
        {
            "what": "The Home Office decides",
            "time": decision_times[speed],
            "sources": [SSW_OVERVIEW, FASTER_DECISION],
        },
    ]
    return {"steps": steps, "weeks": weeks}
