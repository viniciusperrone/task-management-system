from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            obj.delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            model=self.model,
            using=self._db,
        ).filter(is_deleted=False)

    def deleted(self):
        return self.get_queryset().filter(is_deleted=True)

    def include_deleted(self):
        return SoftDeleteQuerySet(
            model=self.model,
            using=self._db,
        )


class BaseModel(models.Model):
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
