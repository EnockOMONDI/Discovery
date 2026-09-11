from django.contrib import admin
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.template.response import TemplateResponse
from .models import DiscoveryResponse
from .questions import FIELD_LOOKUP, QUESTIONS, choice_label

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = "Travel Discovery"
admin.site.index_title = "Discovery responses"


@admin.register(DiscoveryResponse)
class DiscoveryResponseAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("company_name", "contact_person", "email", "phone")
    show_full_result_count = False
    list_per_page = 25
    readonly_fields = (
        "reference", "company_name", "contact_person", "email", "phone", "website", "consent",
        "answers", "created_at", "updated_at",
    )
    fields = (
        "status", "internal_notes", "reference", "company_name", "contact_person", "email", "phone",
        "website", "consent", "answers", "created_at", "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def _render_answer_value(self, field, value):
        if value in ("", None, []):
            return "Not answered"
        if isinstance(value, list):
            return ", ".join(choice_label(field, item) for item in value) or "Not answered"
        if field.get("choices"):
            return choice_label(field, value)
        return str(value)

    def _answer_sections(self, response):
        answers = response.answers or {}
        sections = []
        seen = set()
        for section in QUESTIONS:
            rows = []
            for field in section["fields"]:
                name = field["name"]
                seen.add(name)
                rows.append({
                    "label": field["label"],
                    "value": self._render_answer_value(field, answers.get(name)),
                })
            sections.append({"title": section["title"], "rows": rows})

        extra_rows = []
        for name, value in answers.items():
            if name in seen:
                continue
            field = FIELD_LOOKUP.get(name, {})
            extra_rows.append({
                "label": field.get("label", name.replace("_", " ").title()),
                "value": self._render_answer_value(field, value),
            })
        if extra_rows:
            sections.append({"title": "Other Answers", "rows": extra_rows})
        return sections

    def changelist_view(self, request, extra_context=None):
        query = request.GET.get("q", "").strip()
        responses = DiscoveryResponse.objects.order_by("-created_at")
        if query:
            responses = responses.filter(
                Q(company_name__icontains=query)
                | Q(contact_person__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
            )
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Discovery responses",
            "responses": responses[:100],
            "query": query,
        }
        if extra_context:
            context.update(extra_context)
        return TemplateResponse(request, "admin/discovery/discoveryresponse/change_list.html", context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        response = self.get_object(request, object_id)
        if response is None:
            raise Http404("Discovery response not found")
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": response.company_name,
            "response": response,
            "answer_sections": self._answer_sections(response),
        }
        if extra_context:
            context.update(extra_context)
        return TemplateResponse(request, "admin/discovery/discoveryresponse/change_form.html", context)
