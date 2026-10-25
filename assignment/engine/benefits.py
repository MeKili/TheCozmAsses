from decimal import Decimal

from assignment.rules import BENEFIT_TYPES, FLIGHTS, REMOVAL_COSTS


def yearly_costs(benefit, years, exchange_rate):
    amount = benefit["amount"]
    if benefit["currency"] == "CHF":
        amount = amount / exchange_rate
    if benefit["paid"] == "per month":
        amount = amount * 12
    if benefit["paid"] == "once in year 1":
        return [amount] + [Decimal(0)] * (years - 1)
    return [amount] * years


def benefit_rows(benefits, years, exchange_rate, flights):
    """Works out the cost and the UK taxable part of every benefit in every year.

    Moving costs and temporary housing are removal costs. The employer can pay
    8,000 of them tax free for the whole move, in the order they are listed.
    The flights of the employee are not taxed and do not use up the 8,000.
    """
    limit_left = REMOVAL_COSTS["limit"]
    rows = []
    for benefit in benefits:
        kind = BENEFIT_TYPES[benefit["type"]]
        treatment = benefit.get("treatment") or kind["treatment"]
        costs = yearly_costs(benefit, years, exchange_rate)
        flights_here = flights if benefit["type"] == "moving" else Decimal(0)

        taxable = []
        for year, cost in enumerate(costs):
            if treatment == "removal costs":
                counted = cost - (flights_here if year == 0 else 0)
                free = min(counted, limit_left)
                limit_left -= free
                taxable.append(counted - free)
            elif treatment == "not taxable in the UK":
                taxable.append(Decimal(0))
            else:
                taxable.append(cost)

        tag = treatment
        note = ""
        sources = kind["sources"]
        if treatment == "removal costs":
            tag = "taxable benefit in kind"
            if sum(taxable) == 0:
                tag = "not taxable in the UK"
            elif sum(taxable) < sum(costs):
                tag = "part taxable benefit in kind"
                limit = f"{REMOVAL_COSTS['limit']:,.0f}"
                note = f"Only {limit} of removal costs for a move is tax free. The rest is taxable."
            if flights_here:
                note += " The flights of the employee are not taxed and do not use up the limit."
                sources = sources + FLIGHTS["sources"]

        rows.append(
            {
                "name": benefit["name"],
                "cost": costs,
                "taxable": taxable,
                "tag": tag,
                "taxable_is_cash": treatment == "taxable cash",
                "note": note.strip(),
                "sources": sources,
            }
        )
    return rows
