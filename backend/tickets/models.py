from django.conf import settings
from django.db import models, transaction
from django.db.models import Max

from base.models import BaseModel

from tickets.choices import Priority


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
