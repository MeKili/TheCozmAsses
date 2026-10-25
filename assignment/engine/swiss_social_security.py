from assignment.rules import SWISS_SOCIAL_SECURITY as RULES


def swiss_social_security(pay):
    """Swiss social security for one side, the employee or the employer.

    Both sides pay the same amount. Unemployment insurance is only charged on
    pay up to the limit, the rest is charged on all of the pay.
    """
    ahv_iv_eo = pay * RULES["ahv_iv_eo_rate"]
    alv = min(pay, RULES["alv_max_pay"]) * RULES["alv_rate"]
    return {"ahv_iv_eo": ahv_iv_eo, "alv": alv, "total": ahv_iv_eo + alv}
