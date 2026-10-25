from decimal import Decimal

UK_INCOME_TAX = {
    "personal_allowance": Decimal(12570),
    "taper_starts": Decimal(100000),
    "basic_rate_limit": Decimal(37700),
    "higher_rate_limit": Decimal(125140),
    "basic_rate": Decimal("0.20"),
    "higher_rate": Decimal("0.40"),
    "additional_rate": Decimal("0.45"),
    "sources": [
        {
            "title": "Income Tax rates and Personal Allowances",
            "url": "https://www.gov.uk/income-tax-rates",
        },
        {
            "title": "Rates and thresholds for employers 2026 to 2027",
            "url": "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027",
        },
    ],
}

UK_GROSS_UP = {
    "sources": [
        {
            "title": "PAYE72028: how to gross up",
            "url": "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye72028",
        },
        {
            "title": "Tax equalisation (HS212) 2026",
            "url": "https://www.gov.uk/government/publications/tax-equalisation-hs212-self-assessment-helpsheet/tax-equalisation-2026-hs212",
        },
    ],
}
