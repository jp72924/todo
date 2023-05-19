from django.db import models
from .utils import localtime


class PendingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=Task.Status.PENDING)


class PriotityManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(important=True)


class Task(models.Model):

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        PENDING = 'pending', 'Pending'

    title = models.CharField(max_length=80)
    descrip = models.CharField('description', max_length=280)
    status = models.CharField(max_length=7,
        choices=Status.choices,
        default=Status.PENDING)

    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=localtime())

    important = models.BooleanField(default=False)

    objects = models.Manager()
    pending = PendingManager()
    priority = PriotityManager()

    def is_overdue(self):
        now = localtime()
        return self.due_date < now.date()

    def time_left(self):
        now = localtime()
        return self.due_date - now.date()

    class Meta:
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['due_date'])
        ]

    def __str__(self):
        return self.title
