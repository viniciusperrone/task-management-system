from django.contrib import admin

from tickets.models import Board, Column, Ticket, TicketColumnTransition


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1
    fields = ('name', 'position', 'color')
    ordering = ('position',)


class TicketColumnTransitionInline(admin.TabularInline):
    model = TicketColumnTransition
    extra = 0
    readonly_fields = ('from_column', 'to_column', 'author', 'info', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'formatted_number',
        'title',
        'column_board',
        'column',
        'priority',
        'owner',
        'due_date',
        'updated_at'
    )
    list_filter = ('column__board', 'column', 'priority', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'owner__email')
    autocomplete_fields = ('column', 'owner', 'shared_users')
    filter_horizontal = ('shared_users',)
    readonly_fields = ('number', 'created_at', 'updated_at')
    ordering = ('-priority', 'due_date', 'created_at')

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
            "Kanban",
            {
                "fields": (
                    "column",
                    "position",
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

    @admin.display(description="Board")
    def column_board(self, obj):
        return obj.column.board.name if obj.column else "-"


@admin.register(TicketColumnTransition)
class TicketColumnTransitionAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'from_column', 'to_column', 'author', 'created_at')
    list_filter = ('to_column__board', 'from_column', 'to_column', 'created_at')
    search_fields = ('ticket__title', 'ticket__number', 'author__username', 'author__email', 'info')
    readonly_fields = ('ticket', 'from_column', 'to_column', 'author', 'info', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
