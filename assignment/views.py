from django.shortcuts import render

from assignment.engine.cost_table import cost_table
from assignment.engine.immigration import immigration_costs, immigration_steps
from assignment.forms import CostForm, ImmigrationForm, flatten
from assignment.rules import IMMIGRATION_CARDS
from assignment.test_case import TEST_CASE

IMMIGRATION_DEFAULTS = {
    "years": 2,
    "company_size": "large",
    "has_licence": False,
    "speed": "standard",
}


def cost_estimate(request):
    data = request.GET
    if "test_case" in data:
        data = flatten(TEST_CASE)

    form = CostForm(data or None)
    table = cost_table(form.cleaned_data) if form.is_valid() else None
    return render(request, "assignment/cost.html", {"tab": "cost", "form": form, "table": table})


def immigration(request):
    data = {"years": 2, "company_size": "large", "speed": "standard"}
    data.update(request.GET.dict())

    form = ImmigrationForm(data)
    choices = form.cleaned_data if form.is_valid() else IMMIGRATION_DEFAULTS
    costs = immigration_costs(
        choices["years"], choices["company_size"], choices["has_licence"], choices["speed"]
    )
    steps = immigration_steps(choices["has_licence"], choices["speed"])
    return render(
        request,
        "assignment/immigration.html",
        {"tab": "immigration", "form": form, "cards": IMMIGRATION_CARDS, "costs": costs, "steps": steps},
    )
