from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that performs a soft delete instead of removing records."""
    def delete(self):
        return self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )


class SoftDeleteManager(models.Manager):
    """Manager that hides soft-deleted objects by default."""
    def get_queryset(self):
        return SoftDeleteQuerySet(
            model=self.model,
            using=self._db,
        ).filter(is_deleted=False)

    def deleted(self):
        return self.include_deleted().filter(is_deleted=True)

    def include_deleted(self):
        return SoftDeleteQuerySet(
            model=self.model,
            using=self._db,
        )


class BaseModel(models.Model):
    """Abstract base model that provides timestamp fields and soft delete support."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
