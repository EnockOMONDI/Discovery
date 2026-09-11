from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .models import DiscoveryResponse
from .questions import FIELD_LOOKUP, QUESTIONS


def _collect_answers(post_data):
    answers = {}
    errors = {}
    for name, field in FIELD_LOOKUP.items():
        if field["type"] == "checkboxes":
            value = [item for item in post_data.getlist(name) if item]
        else:
            value = post_data.get(name, "").strip()
        if field.get("required") and not value:
            errors[name] = "Please answer this before submitting."
        answers[name] = value

    if answers.get("email"):
        try:
            validate_email(answers["email"])
        except ValidationError:
            errors["email"] = "Enter a valid email address."

    if post_data.get("company_site", ""):
        errors["__all__"] = "Unable to accept this submission."

    if post_data.get("consent") != "yes":
        errors["consent"] = "Please confirm that these answers can be stored for follow-up."

    return answers, errors


@require_http_methods(["GET", "POST"])
def discovery_form(request):
    values = {}
    errors = {}
    error_step = 0
    if request.method == "POST":
        values, errors = _collect_answers(request.POST)
        if not errors:
            response = DiscoveryResponse.objects.create(
                company_name=values["company_name"],
                contact_person=values["contact_person"],
                email=values["email"],
                phone=values.get("phone", ""),
                website=values.get("website", ""),
                answers=values,
                consent=True,
            )
            return redirect("discovery_thanks", reference=response.reference)
        for index, section in enumerate(QUESTIONS):
            if any(field["name"] in errors for field in section["fields"]):
                error_step = index
                break
    return render(request, "discovery/form.html", {
        "sections": QUESTIONS,
        "values": values,
        "errors": errors,
        "error_step": error_step,
    })


def discovery_thanks(request, reference):
    return render(request, "discovery/thanks.html", {"reference": reference})

# Create your views here.
