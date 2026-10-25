from datetime import date
from decimal import Decimal

TEST_CASE = {
    "start": date(2026, 4, 6),
    "end": date(2028, 4, 5),
    "salary": Decimal(150000),
    "bonus": Decimal(20000),
    "exchange_rate": Decimal("1.10"),
    "pension": Decimal(0),
    "flights": Decimal(0),
    "replaces_another_worker": False,
    "benefits": [
        {
            "name": "Housing in London",
            "type": "housing",
            "amount": Decimal(3000),
            "currency": "GBP",
            "paid": "per month",
        },
        {
            "name": "Relocation allowance",
            "type": "cash",
            "amount": Decimal(5000),
            "currency": "CHF",
            "paid": "once in year 1",
        },
        {
            "name": "Moving costs (flights, shipping)",
            "type": "moving",
            "amount": Decimal(6000),
            "currency": "GBP",
            "paid": "once in year 1",
        },
        {
            "name": "Temporary housing (serviced apartment, 4 weeks)",
            "type": "temporary_housing",
            "amount": Decimal(4000),
            "currency": "GBP",
            "paid": "once in year 1",
        },
    ],
}
