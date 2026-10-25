from datetime import timedelta

from dateutil.relativedelta import relativedelta

from assignment.rules import SOCIAL_SECURITY_RULE as RULES


def social_security_rule(start, end, replaces_another_worker):
    """Decides which country's social security applies during the assignment.

    A worker sent by a Swiss employer stays in Swiss social security if the
    work lasts no more than 24 months and does not replace another posted
    worker. Otherwise UK National Insurance is due from the first day.
    """
    length = relativedelta(end + timedelta(days=1), start)
    months = length.years * 12 + length.months
    lasts = f"{months} months"
    if length.days:
        lasts += f" and {length.days} day" + ("s" if length.days > 1 else "")

    too_long = end >= start + relativedelta(months=RULES["max_months"])

    if replaces_another_worker:
        country = "United Kingdom"
        reason = (
            "The employee replaces another posted worker, so the 24 month rule "
            "does not apply. UK National Insurance is due from the first day."
        )
    elif too_long:
        country = "United Kingdom"
        reason = (
            f"The assignment lasts {lasts}, which is more than 24 months. "
            "UK National Insurance is due from the first day. Both countries "
            "can agree an exception, which this tool does not work out."
        )
    else:
        country = "Switzerland"
        reason = (
            f"The assignment lasts {lasts}, which is not more than 24 months, "
            "and the employee does not replace another posted worker. Swiss "
            "social security keeps applying and no UK National Insurance is "
            "due. The employer asks its Swiss compensation fund for a "
            "certificate of coverage."
        )

    return {
        "country": country,
        "months": months,
        "reason": reason,
        "sources": RULES["sources"],
    }
