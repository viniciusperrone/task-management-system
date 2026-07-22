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


class Ticket(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Texto", blank=True)
    priority = models.IntegerField(choices=Priority, default=Priority.MEDIUM, verbose_name="Prioridade")
    due_date = models.DateField(verbose_name="Data de vencimento", null=True, blank=True, db_index=True)
    number = models.PositiveIntegerField(unique=True, db_index=True, editable=False, verbose_name="Número")
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
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.formatted_number} - {self.title}"
