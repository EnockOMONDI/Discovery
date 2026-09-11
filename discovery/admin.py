from django.contrib import admin
from django.conf import settings
from django.db.models import Q
from django.template.response import TemplateResponse
from .models import DiscoveryResponse

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
