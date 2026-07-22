from django.contrib import admin

from tickets.models import Board, Column, Ticket


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

class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1
    fields = ('name', 'position', 'color')
    ordering = ('position',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'color', 'created_at', 'updated_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'description', 'owner__username', 'owner__email')
    autocomplete_fields = ('owner',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ColumnInline]

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "name",
                    "description",
                    "color",
                    "owner",
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


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'position', 'color', 'updated_at')
    list_filter = ('board', 'created_at')
    search_fields = ('name', 'board__name')
    autocomplete_fields = ('board',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('board', 'position')