from datetime import timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django import forms

from assignment.rules import BENEFIT_TYPES

BENEFIT_ROWS = 6
BENEFIT_PARTS = ["name", "type", "amount", "currency", "paid", "treatment"]
MAX_YEARS = 5

HOME_COUNTRIES = [
    ("CH", "Switzerland"),
    ("DE", "Germany (not supported yet)"),
    ("FR", "France (not supported yet)"),
    ("US", "United States (not supported yet)"),
]
HOST_COUNTRIES = [
    ("GB", "United Kingdom"),
    ("DE", "Germany (not supported yet)"),
    ("FR", "France (not supported yet)"),
    ("US", "United States (not supported yet)"),
]
TREATMENTS = [
    ("", "Default"),
    ("taxable cash", "Taxable cash"),
    ("taxable benefit in kind", "Taxable benefit"),
    ("not taxable in the UK", "Not taxable"),
]


class CountrySelect(forms.Select):
    """A dropdown that shows other countries but only lets you pick one."""

    def __init__(self, supported):
        super().__init__()
        self.supported = supported

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value != self.supported:
            option["attrs"]["disabled"] = True
        return option


class CostForm(forms.Form):
    home_country = forms.ChoiceField(
        label="Home country",
        choices=HOME_COUNTRIES,
        widget=CountrySelect("CH"),
        initial="CH",
    )
    host_country = forms.ChoiceField(
        label="Host country",
        choices=HOST_COUNTRIES,
        widget=CountrySelect("GB"),
        initial="GB",
    )
    start = forms.DateField(
        label="Assignment starts",
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        help_text="The first day in the host country.",
    )
    end = forms.DateField(
        label="Assignment ends",
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        help_text="The last day. A whole number of years, for example 6 April 2026 to 5 April 2028.",
    )
    replaces_another_worker = forms.BooleanField(
        required=False,
        label="The employee replaces another posted worker",
        help_text="If yes, the 24 month rule for Swiss social security does not apply.",
    )
    salary = forms.DecimalField(
        label="Base salary (CHF a year)",
        min_value=0,
        help_text="The yearly salary the employee gets at home.",
    )
    bonus = forms.DecimalField(
        label="Bonus (CHF a year)",
        min_value=0,
        required=False,
        initial=0,
        help_text="Leave empty if there is no bonus.",
    )
    exchange_rate = forms.DecimalField(
        label="Exchange rate: GBP 1 is how many CHF",
        min_value=Decimal("0.01"),
        error_messages={"min_value": "The exchange rate must be more than 0."},
        help_text="Francs are divided by this number to get pounds.",
    )
    pension = forms.DecimalField(
        label="Pension fund and accident insurance (CHF a year)",
        min_value=0,
        required=False,
        initial=0,
        help_text="What the employee pays into a pension fund and accident insurance at home. "
        "The pack leaves the pension fund out, so the default is 0.",
    )
    flights = forms.DecimalField(
        label="Of the moving costs, the flights of the employee (GBP)",
        min_value=0,
        required=False,
        initial=0,
        help_text="Flights of the employee to the UK are not taxed and do not use up the "
        "tax free limit for removal costs. Leave 0 if you do not know.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        type_choices = [(key, kind["label"]) for key, kind in BENEFIT_TYPES.items()]
        for i in range(1, BENEFIT_ROWS + 1):
            self.fields[f"benefit_{i}_name"] = forms.CharField(
                required=False, max_length=60, widget=forms.TextInput(attrs={"placeholder": "Name"})
            )
            self.fields[f"benefit_{i}_type"] = forms.ChoiceField(
                choices=type_choices, initial="other", required=False
            )
            self.fields[f"benefit_{i}_amount"] = forms.DecimalField(
                required=False, min_value=0
            )
            self.fields[f"benefit_{i}_currency"] = forms.ChoiceField(
                choices=[("GBP", "GBP"), ("CHF", "CHF")], initial="GBP", required=False
            )
            self.fields[f"benefit_{i}_paid"] = forms.ChoiceField(
                choices=[("per month", "per month"), ("per year", "per year"), ("once in year 1", "once, year 1")],
                initial="once in year 1",
                required=False,
            )
            self.fields[f"benefit_{i}_treatment"] = forms.ChoiceField(
                choices=TREATMENTS, required=False
            )

        if self.is_bound:
            for name in self.errors:
                self.fields[name].widget.attrs["aria-invalid"] = "true"

    def benefit_rows(self):
        return [
            [self[f"benefit_{i}_{part}"] for part in BENEFIT_PARTS]
            for i in range(1, BENEFIT_ROWS + 1)
        ]

    def clean(self):
        data = super().clean()
        for name in ("bonus", "pension", "flights"):
            if data.get(name) is None:
                data[name] = Decimal(0)
        self.check_dates(data)
        data["benefits"] = self.read_benefits(data)
        return data

    def check_dates(self, data):
        start, end = data.get("start"), data.get("end")
        if not start or not end:
            return
        if end <= start:
            self.add_error("end", "The end date must be after the start date.")
            return
        length = relativedelta(end + timedelta(days=1), start)
        if length.months or length.days:
            self.add_error(
                "end",
                "The assignment must last a whole number of years, for example "
                f"6 April 2026 to 5 April 2028. These dates give {length.years} years, "
                f"{length.months} months and {length.days} days.",
            )
        elif length.years > MAX_YEARS:
            self.add_error("end", f"This tool works for assignments of up to {MAX_YEARS} years.")

    def read_benefits(self, data):
        benefits = []
        for i in range(1, BENEFIT_ROWS + 1):
            name = data.get(f"benefit_{i}_name")
            amount = data.get(f"benefit_{i}_amount")
            if not name and amount is None:
                continue
            if not name:
                self.add_error(f"benefit_{i}_name", "Give this benefit a name, or empty the row.")
            elif amount is None:
                self.add_error(f"benefit_{i}_amount", "Give the amount of this benefit, or empty the row.")
            else:
                benefits.append(
                    {
                        "name": name,
                        "type": data.get(f"benefit_{i}_type") or "other",
                        "amount": amount,
                        "currency": data.get(f"benefit_{i}_currency") or "GBP",
                        "paid": data.get(f"benefit_{i}_paid") or "once in year 1",
                        "treatment": data.get(f"benefit_{i}_treatment", ""),
                    }
                )
        return benefits


def flatten(inputs):
    """Turns the inputs of the engine into the fields of the form."""
    data = {
        "home_country": "CH",
        "host_country": "GB",
        "start": inputs["start"].isoformat(),
        "end": inputs["end"].isoformat(),
        "salary": inputs["salary"],
        "bonus": inputs["bonus"],
        "exchange_rate": inputs["exchange_rate"],
        "pension": inputs["pension"],
        "flights": inputs["flights"],
    }
    if inputs["replaces_another_worker"]:
        data["replaces_another_worker"] = "on"
    for i, benefit in enumerate(inputs["benefits"], start=1):
        for part in BENEFIT_PARTS:
            data[f"benefit_{i}_{part}"] = benefit.get(part, "")
    return data


class ImmigrationForm(forms.Form):
    years = forms.IntegerField(
        label="Length of the stay in years",
        min_value=1,
        max_value=MAX_YEARS,
        initial=2,
    )
    company_size = forms.ChoiceField(
        label="Size of the UK company",
        choices=[("large", "Medium or large company"), ("small", "Small company or charity")],
        initial="large",
        help_text="A company is small if at least 2 of these are true: a turnover of 15 million "
        "pounds or less, assets of 7.5 million pounds or less, 50 employees or fewer.",
    )
    has_licence = forms.BooleanField(
        required=False,
        label="The UK company already has a sponsor licence",
    )
    speed = forms.ChoiceField(
        label="Speed of the visa decision",
        choices=[
            ("standard", "Standard"),
            ("priority", "Priority service"),
            ("super priority", "Super priority service"),
        ],
        initial="standard",
    )
