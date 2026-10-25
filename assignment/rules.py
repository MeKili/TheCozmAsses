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

GOV = "https://www.gov.uk/"

SSW_OVERVIEW = {
    "title": "Senior or Specialist Worker visa: overview",
    "url": GOV + "senior-specialist-worker-visa",
}
SSW_ELIGIBILITY = {
    "title": "Senior or Specialist Worker visa: eligibility",
    "url": GOV + "senior-specialist-worker-visa/eligibility",
}
SSW_COSTS = {
    "title": "Senior or Specialist Worker visa: how much it costs",
    "url": GOV + "senior-specialist-worker-visa/how-much-it-costs",
}
SPONSOR_OVERVIEW = {
    "title": "UK visa sponsorship for employers",
    "url": GOV + "uk-visa-sponsorship-employers",
}
SPONSOR_LICENCE = {
    "title": "Apply for a sponsor licence: fees and how long it takes",
    "url": GOV + "uk-visa-sponsorship-employers/apply-for-your-licence",
}
CERTIFICATES = {
    "title": "Certificates of sponsorship and what they cost",
    "url": GOV + "uk-visa-sponsorship-employers/certificates-of-sponsorship",
}
SKILLS_CHARGE = {
    "title": "Immigration skills charge",
    "url": GOV + "uk-visa-sponsorship-employers/immigration-skills-charge",
}
FASTER_DECISION = {
    "title": "Get a faster decision on your visa",
    "url": GOV + "faster-decision-visa-settlement",
}
ETA_OVERVIEW = {
    "title": "Get an electronic travel authorisation (ETA)",
    "url": GOV + "eta",
}
ETA_APPLY = {
    "title": "Apply for an ETA",
    "url": GOV + "eta/apply",
}
VISIT_ON_BUSINESS = {
    "title": "Visit the UK as a Standard Visitor: visit on business",
    "url": GOV + "standard-visitor/visit-on-business",
}
VISITOR_ACTIVITIES = {
    "title": "Immigration Rules: Appendix Visitor, permitted activities",
    "url": GOV + "guidance/immigration-rules/immigration-rules-appendix-visitor-permitted-activities",
}
SWISS_VISITORS = {
    "title": "Visiting the UK as an EU, EEA or Swiss citizen",
    "url": GOV + "guidance/visiting-the-uk-as-an-eu-eea-or-swiss-citizen",
}
PAYE_PAGE = UK_EMPLOYER_NI["sources"][0]
SWISS_CERTIFICATE = SOCIAL_SECURITY_RULE["sources"][0]
SWISS_FUND = SOCIAL_SECURITY_RULE["sources"][2]

IMMIGRATION_COSTS = {
    "visa_fee_up_to_3_years": Decimal(819),
    "visa_fee_over_3_years": Decimal(1618),
    "health_surcharge_per_year": Decimal(1035),
    "certificate_of_sponsorship": Decimal(525),
    "skills_charge_first_12_months": {"large": Decimal(1320), "small": Decimal(480)},
    "skills_charge_each_extra_6_months": {"large": Decimal(660), "small": Decimal(240)},
    "sponsor_licence": {"large": Decimal(1682), "small": Decimal(611)},
    "faster_decision": {"standard": Decimal(0), "priority": Decimal(500), "super priority": Decimal(1000)},
    "weeks_for_decision": {"standard": 3, "priority": 1, "super priority": 0},
    "weeks_for_licence": 8,
    "savings_needed": Decimal(1270),
}

IMMIGRATION_CARDS = [
    {
        "title": "Work permit",
        "answer": "The employee needs a Senior or Specialist Worker visa (Global Business Mobility) "
        "before starting work in the UK. It is the visa for an employee that a group sends to its UK company.",
        "points": [
            {
                "text": "The employee already works for the group and is sponsored by the UK company. "
                "The UK company must be approved by the Home Office as a sponsor and gives the employee "
                "a certificate of sponsorship.",
                "sources": [SSW_OVERVIEW, SSW_ELIGIBILITY],
            },
            {
                "text": "The job must be on the list of eligible jobs and pay at least 52,500 pounds a year, "
                "or the going rate for the job if that is higher.",
                "sources": [SSW_ELIGIBILITY],
            },
            {
                "text": "The employee must have worked for the group outside the UK for at least 12 months. "
                "This is not needed at 73,900 pounds a year or more.",
                "sources": [SSW_ELIGIBILITY],
            },
            {
                "text": "The employee can stay up to 5 years in any 6 years, or up to 9 years in any 10 years "
                "at 73,900 pounds a year or more.",
                "sources": [SSW_OVERVIEW],
            },
            {
                "text": "The employee applies online, up to 3 months before the start date and within 3 months "
                "of getting the certificate of sponsorship.",
                "sources": [SSW_OVERVIEW, SSW_ELIGIBILITY],
            },
            {
                "text": "The employee must show at least 1,270 pounds in savings, unless the employer says on "
                "the certificate that it pays the costs of the first month.",
                "sources": [SSW_COSTS],
            },
            {
                "text": "The certificate of coverage from the Swiss compensation fund is not a work permit.",
                "sources": [SWISS_CERTIFICATE],
            },
        ],
    },
    {
        "title": "Business visit before the assignment (business visa)",
        "answer": "No visa is needed for a business visit. A Swiss citizen needs an electronic travel "
        "authorisation (ETA) instead. It costs 20 pounds, lasts 2 years or until the passport ends, "
        "and allows visits of up to 6 months.",
        "points": [
            {
                "text": "The ETA is linked to the passport. The employee applies online or in the UK ETA app. "
                "A decision usually comes within a day and can take up to 3 working days.",
                "sources": [ETA_OVERVIEW, ETA_APPLY, SWISS_VISITORS],
            },
            {
                "text": "Allowed: meetings, conferences, seminars and interviews, negotiating and signing deals "
                "and contracts, work related training, site visits and inspections, and advising, training "
                "or sharing skills on a specific internal project with UK employees of the same group.",
                "sources": [VISIT_ON_BUSINESS, VISITOR_ACTIVITIES],
            },
            {
                "text": "Not allowed: any other paid or unpaid work in the UK, or being paid by a UK "
                "organisation for the visit. Working for the UK company needs the work visa first.",
                "sources": [VISIT_ON_BUSINESS],
            },
        ],
    },
    {
        "title": "Passport",
        "answer": "The employee needs a valid passport that covers the whole time in the UK. "
        "A Swiss national identity card is not enough.",
        "points": [
            {
                "text": "A passport, or in a few listed cases a national identity card, valid for the whole "
                "stay. Identity cards only work for people with EU Settlement Scheme status, a frontier "
                "worker permit and similar groups.",
                "sources": [SWISS_VISITORS],
            },
            {
                "text": "The ETA is linked to the passport used to apply. The employee shows that passport "
                "when travelling.",
                "sources": [ETA_APPLY],
            },
        ],
    },
    {
        "title": "What the company must do",
        "answer": "",
        "points": [
            {
                "text": "The UK company needs a sponsor licence if it has none. It checks that it is eligible "
                "and that the job is suitable, chooses the Worker licence, decides who manages sponsorship "
                "in the business, applies online and pays the fee.",
                "sources": [SPONSOR_OVERVIEW, SPONSOR_LICENCE],
            },
            {
                "text": "The UK company assigns a certificate of sponsorship to the employee and pays the "
                "certificate fee and the immigration skills charge. It must pay the licence fee, the "
                "certificate and the skills charge itself and may not ask the worker to pay them.",
                "sources": [CERTIFICATES, SKILLS_CHARGE, SPONSOR_LICENCE],
            },
            {
                "text": "The Swiss employer asks its Swiss compensation fund for a certificate of coverage "
                "and keeps it. It is the proof that no UK National Insurance is due.",
                "sources": [SWISS_CERTIFICATE, SWISS_FUND],
            },
            {
                "text": "The UK company runs the pay of the employee through its UK payroll (PAYE), and reports "
                "it to HMRC the way HMRC asks for tax equalised employees.",
                "sources": [PAYE_PAGE, UK_GROSS_UP["sources"][1]],
            },
        ],
    },
]
