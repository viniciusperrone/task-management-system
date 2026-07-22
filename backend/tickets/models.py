from django.conf import settings
from django.db import models, transaction
from django.db.models import Max

from base.models import BaseModel

from tickets.choices import Priority


class Board(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boards",
    )
    color = models.CharField(
        max_length=7,
        default="#3B82F6",
        verbose_name="Cor",
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("owner", "name")
        verbose_name = "Board"
        verbose_name_plural = "Boards"

    def __str__(self):
        return self.name


class Column(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nome")
    position = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Posição")
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Cor")
    board = models.ForeignKey(
        "tickets.Board",
        on_delete=models.CASCADE,
        related_name="columns",
    )

    class Meta:
        ordering = ["board", "position"]
        verbose_name = "Coluna"
        verbose_name_plural = "Colunas"

    def __str__(self):
        return f"{self.board.name} -> {self.name}"


class Ticket(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Texto", blank=True)
    priority = models.IntegerField(choices=Priority, default=Priority.MEDIUM, verbose_name="Prioridade")
    due_date = models.DateField(verbose_name="Data de vencimento", null=True, blank=True, db_index=True)
    number = models.PositiveIntegerField(unique=True, db_index=True, editable=False, verbose_name="Número")

    column = models.ForeignKey(
        "tickets.Column",
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Coluna",
        null=True,
        blank=True,
    )
    position = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Posição na coluna")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    shared_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="shared_tickets",
    )

    @property
    def formatted_number(self):
        return f"#{self.number:04d}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            with transaction.atomic():
                last_number = (
                    Ticket.objects.include_deleted().
                    aggregate(max_number=Max("number"))["max_number"] or 0
                )
                self.number = last_number + 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-priority", "due_date", "created_at"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"{self.formatted_number} - {self.title}"


class TicketColumnTransition(BaseModel):
    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="transitions",
        verbose_name="Ticket"
    )
    from_column = models.ForeignKey(
        "tickets.Column",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transitions_from",
        verbose_name="Coluna de Origem"
    )
    to_column = models.ForeignKey(
        "tickets.Column",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transitions_to",
        verbose_name="Coluna Destino"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Autor de Transição"
    )
    info = models.TextField(blank=True, default="", verbose_name="Informações Adicionais")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transição de Ticket"
        verbose_name_plural = "Transições de Ticket"

    def __str__(self):
        author_name = self.author.username if self.author else "Sistema"
        from_name = self.from_column.name if self.from_column else "Sem Coluna"

        return f"Ticket #{self.ticket.number:04d}: {from_name} -> {self.to_column.name} por {author_name}"

    @classmethod
    def execute_transition(cls, ticket, to_column, author=None, info=""):
        if ticket.column_id == to_column.id:
            return None

        from_column = ticket.column

        with transaction.atomic():
            transition_obj = cls.objects.create(
                ticket=ticket,
                from_column=from_column,
                to_column=to_column,
                author=author,
                info=info,
            )

            ticket.column = to_column
            ticket.save(update_fields=["column", "updated_at"])

        return transition_obj
