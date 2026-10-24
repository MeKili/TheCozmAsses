from decimal import Decimal

from assignment.engine.uk_tax import uk_tax


def gross_up(income):
    """Works out the UK tax the employer pays when it pays the tax too.

    The tax the employer pays is taxable pay as well. So we add the tax to the
    income, work out the tax again, and repeat until the answer stops moving.
    Returns the tax and the answer of every round, for the working on screen.
    """
    tax = Decimal(0)
    rounds = []
    while True:
        new_tax = uk_tax(income + tax)
        rounds.append(new_tax)
        if abs(new_tax - tax) < Decimal("0.00001"):
            return new_tax, rounds
        tax = new_tax
