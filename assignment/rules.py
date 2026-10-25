from decimal import Decimal

INFINITY = Decimal("Infinity")

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

SWISS_SOCIAL_SECURITY = {
    "ahv_iv_eo_rate": Decimal("0.053"),
    "alv_rate": Decimal("0.011"),
    "alv_max_pay": Decimal(148200),
    "sources": [
        {
            "title": "Swiss social insurance contribution rates 2026",
            "url": "https://sozialversicherungen.admin.ch/de/d/6877/download",
        },
    ],
}

SWISS_TAX = {
    "federal_slices": [
        (Decimal(15200), Decimal("0")),
        (Decimal(18000), Decimal("0.0077")),
        (Decimal(10300), Decimal("0.0088")),
        (Decimal(14500), Decimal("0.0264")),
        (Decimal(18200), Decimal("0.0297")),
        (Decimal(5900), Decimal("0.0594")),
        (Decimal(26800), Decimal("0.066")),
        (Decimal(32600), Decimal("0.088")),
        (Decimal(43600), Decimal("0.11")),
        (INFINITY, Decimal("0.132")),
    ],
    "federal_flat_from": Decimal(793900),
    "federal_flat_rate": Decimal("0.115"),
    "zurich_slices": [
        (Decimal(7000), Decimal("0")),
        (Decimal(5000), Decimal("0.02")),
        (Decimal(4800), Decimal("0.03")),
        (Decimal(8000), Decimal("0.04")),
        (Decimal(9700), Decimal("0.05")),
        (Decimal(11200), Decimal("0.06")),
        (Decimal(13100), Decimal("0.07")),
        (Decimal(17600), Decimal("0.08")),
        (Decimal(34000), Decimal("0.09")),
        (Decimal(33700), Decimal("0.10")),
        (Decimal(53300), Decimal("0.11")),
        (Decimal(69300), Decimal("0.12")),
        (INFINITY, Decimal("0.13")),
    ],
    "canton_multiplier": Decimal("0.95"),
    "city_multiplier": Decimal("1.19"),
    "work_costs_rate": Decimal("0.03"),
    "work_costs_min": Decimal(2000),
    "work_costs_max": Decimal(4000),
    "insurance_deduction_without_pension": {
        "federal": Decimal(2700),
        "canton": Decimal(4350),
    },
    "insurance_deduction_with_pension": {
        "federal": Decimal(1800),
        "canton": Decimal(2900),
    },
    "sources": [
        {
            "title": "Federal tax tariff 2026 (form 58c)",
            "url": "https://www.estv.admin.ch/dam/de/sd-web/gnde9CmEsalK/dbst-tairfe-58c-2026-dfi.pdf",
        },
        {
            "title": "Federal tax deductions 2026 (ESTV circular)",
            "url": "https://www.estv.admin.ch/dam/de/sd-web/vFK3ntWLQ4s4/2-215-D-2025-d.pdf",
        },
        {
            "title": "Canton Zurich tax tariff and deductions 2026",
            "url": "https://www.estv2.admin.ch/stp/kb/zh-de.pdf",
        },
        {
            "title": "Tax multipliers 2026 (ESTV)",
            "url": "https://www.estv2.admin.ch/stp/ds/e-steuersatz-steuerfuss-de.pdf",
        },
    ],
}

SOCIAL_SECURITY_RULE = {
    "max_months": 24,
    "sources": [
        {
            "title": "GOV.UK: paying social security if you come to work in the UK from Switzerland",
            "url": "https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland",
        },
        {
            "title": "UK and Switzerland social security convention, Article 14",
            "url": "https://assets.publishing.service.gov.uk/media/6697bfdaa3c2a28abb50d14e/TS_47.2024_UK_Switzerland_Convention_Social_Security_Coordination_with_corrections.pdf",
        },
        {
            "title": "AHV/IV information centre: posting from Switzerland (leaflet 10.01)",
            "url": "https://www.ahv-iv.ch/p/10.01.d",
        },
    ],
}

EIM_URL = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/"

EIM03102 = {"title": "EIM03102: removal costs, charging provisions", "url": EIM_URL + "eim03102"}
EIM03103 = {"title": "EIM03103: removal costs, the exemption from charge", "url": EIM_URL + "eim03103"}
EIM03111 = {"title": "EIM03111: removal costs, transporting belongings", "url": EIM_URL + "eim03111"}
EIM03116 = {"title": "EIM03116: removal costs, international moves", "url": EIM_URL + "eim03116"}
EIM03117 = {"title": "EIM03117: removal costs, temporary living accommodation", "url": EIM_URL + "eim03117"}
EIM00580 = {"title": "EIM00580: employer paying the employee's debt", "url": EIM_URL + "eim00580"}
EIM35030 = {"title": "EIM35030: travel between the home country and the UK", "url": EIM_URL + "eim35030"}

UK_EMPLOYER_NI = {
    "secondary_threshold": Decimal(5000),
    "employer_rate": Decimal("0.15"),
    "class_1a_rate": Decimal("0.15"),
    "sources": [
        {
            "title": "Rates and thresholds for employers 2026 to 2027",
            "url": "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027",
        },
    ],
}

REMOVAL_COSTS = {
    "limit": Decimal(8000),
    "sources": [EIM03103, EIM03111, EIM03117],
}

FLIGHTS = {
    "sources": [EIM03116, EIM35030],
}

BENEFIT_TYPES = {
    "housing": {
        "label": "Housing",
        "treatment": "taxable benefit in kind",
        "sources": [EIM00580, EIM03117],
    },
    "cash": {
        "label": "Cash allowance",
        "treatment": "taxable cash",
        "sources": [EIM03102, EIM03103],
    },
    "moving": {
        "label": "Moving costs",
        "treatment": "removal costs",
        "sources": REMOVAL_COSTS["sources"],
    },
    "temporary_housing": {
        "label": "Temporary housing",
        "treatment": "removal costs",
        "sources": REMOVAL_COSTS["sources"],
    },
    "other": {
        "label": "Other benefit",
        "treatment": "taxable cash",
        "sources": [EIM03102],
    },
}

ASSUMPTIONS = [
    {
        "text": "The employee is a Swiss national, single, with no children, and has worked "
        "for the employer in Zurich for 3 years. The employer is Swiss and its UK company runs the UK payroll.",
        "sources": [],
    },
    {
        "text": "The employee is UK tax resident in every year of the assignment. "
        "The rates and limits of 2026 to 2027 are used for every year.",
        "sources": UK_INCOME_TAX["sources"],
    },
    {
        "text": "Every year is a full year. Home pay and monthly benefits are the same in every year. "
        "The exchange rate does not change, and francs are divided by it to get pounds.",
        "sources": [],
    },
    {
        "text": "The employer pays all the UK income tax on the pay and the taxable benefits, in the year "
        "it arises. The tax is itself taxable pay, so it is worked out again and again until the number "
        "stops changing. There is no other income and no other tax relief.",
        "sources": UK_GROSS_UP["sources"],
    },
    {
        "text": "Swiss social security keeps applying when the assignment lasts no more than 24 months and "
        "the employee does not replace another posted worker. Then no UK National Insurance is due and "
        "the Swiss contributions of both sides are a cost. The employer asks its Swiss compensation fund "
        "for a certificate of coverage.",
        "sources": SOCIAL_SECURITY_RULE["sources"],
    },
    {
        "text": "If the assignment is longer than 24 months, or replaces another posted worker, UK National "
        "Insurance is due from the first day. The tool then counts the employer part (15% of pay above "
        "5,000 a year) and 15% on benefits in kind. The part of the employee is not worked out. "
        "Both countries can agree an exception, which is not worked out either.",
        "sources": UK_EMPLOYER_NI["sources"],
    },
    {
        "text": "The hypothetical Swiss tax is the federal, canton and city income tax of a single person in "
        "the city of Zurich, with no church tax and without the personal tax of 24 francs that the official "
        "calculator adds. It uses the tariffs, deductions and tax multipliers of 2026.",
        "sources": SWISS_TAX["sources"],
    },
    {
        "text": "The hypothetical Swiss social security is what the employee would pay at home for AHV, IV, EO "
        "and unemployment insurance. The pension fund is left out as the pack says, unless you enter it.",
        "sources": SWISS_SOCIAL_SECURITY["sources"],
    },
    {
        "text": "Housing paid straight to the landlord is taxed as a benefit in kind. If the tenancy is in the "
        "name of the employee, HMRC taxes it as pay instead. The tax is the same.",
        "sources": BENEFIT_TYPES["housing"]["sources"],
    },
    {
        "text": "A cash allowance is taxable cash pay.",
        "sources": BENEFIT_TYPES["cash"]["sources"],
    },
    {
        "text": "Moving costs and temporary housing are removal costs. The employer can pay 8,000 of them tax "
        "free for one move, in the order they are listed. The flights of the employee are not taxed and do "
        "not use up the 8,000, if the employee is a new UK resident.",
        "sources": REMOVAL_COSTS["sources"] + FLIGHTS["sources"],
    },
    {
        "text": "Immigration costs are on the Immigration tab and are not part of this total.",
        "sources": [],
    },
    {
        "text": "Not worked out: the Swiss family allowance fund, accident insurance and fees of the Swiss "
        "compensation fund, the UK Apprenticeship Levy and Employment Allowance, VAT on the serviced "
        "apartment, advice and tax return fees, home leave, hardship allowances and changes in the "
        "exchange rate.",
        "sources": [],
    },
    {
        "text": "Assumed without a check: the employee was insured in Switzerland for long enough before the "
        "posting, the job is on the UK list of eligible jobs and is paid above its going rate, and the UK "
        "company holds or gets a sponsor licence.",
        "sources": [],
    },
]
