from django.contrib import admin
from django.conf import settings
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
