from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html, format_html_join
from .models import DiscoveryResponse
from .questions import choice_label, FIELD_LOOKUP

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = "Travel Discovery"
admin.site.index_title = "Discovery responses"


@admin.register(DiscoveryResponse)
class DiscoveryResponseAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("company_name", "contact_person", "email", "phone", "answers")
    date_hierarchy = "created_at"
    readonly_fields = (
        "reference", "company_name", "contact_person", "email", "phone", "website", "consent",
        "formatted_answers", "created_at", "updated_at",
    )
    fields = (
        "status", "internal_notes", "reference", "company_name", "contact_person", "email", "phone",
        "website", "consent", "formatted_answers", "created_at", "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formatted_answers(self, obj):
        rows = []
        for key, value in obj.answers.items():
            field = FIELD_LOOKUP.get(key, {})
            label = field.get("label", key.replace("_", " ").title())
            if isinstance(value, list):
                rendered = ", ".join(choice_label(field, item) for item in value)
            else:
                rendered = choice_label(field, value) if field.get("choices") else str(value)
            rendered = rendered or "Not answered"
            rows.append((label, rendered))
        return format_html(
            "<dl class='discovery-answers'>{}</dl>",
            format_html_join("", "<dt>{}</dt><dd>{}</dd>", rows),
        )

    formatted_answers.short_description = "Submitted answers"

    class Media:
        css = {"all": ("discovery/admin.css",)}

# Register your models here.
