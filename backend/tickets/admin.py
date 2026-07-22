from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('formatted_number', 'title', 'priority', 'owner', 'due_date', 'updated_at')
    list_filter = ('priority', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'owner__email')
    autocomplete_fields = ('owner', 'shared_users')
    filter_horizontal = ('shared_users',)
    readonly_fields = ('number', 'created_at', 'updated_at')
    ordering = ('-updated_at',)

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "number",
                    "title",
                    "description",
                    "priority",
                    "due_date",
                )
            },
        ),
        (
            "Ownership",
            {
                "fields": (
                    "owner",
                    "shared_users",
                )
            },
        ),
        (
            "Metadata",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
