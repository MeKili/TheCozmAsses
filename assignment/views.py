from django.shortcuts import render

from assignment.engine.cost_table import cost_table
from assignment.forms import CostForm, flatten
from assignment.test_case import TEST_CASE


def cost_estimate(request):
    data = request.GET
    if "test_case" in data:
        data = flatten(TEST_CASE)

    form = CostForm(data or None)
    table = cost_table(form.cleaned_data) if form.is_valid() else None
    return render(request, "assignment/cost.html", {"form": form, "table": table})
