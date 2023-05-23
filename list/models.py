from django.db import models
from .utils import localtime


class PendingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=Task.Status.PENDING)


class Task(models.Model):

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        PENDING = 'pending', 'Pending'

    title = models.CharField(max_length=80)
    descrip = models.CharField('description', max_length=280)
    status = models.CharField(max_length=7,
        choices=Status.choices,
        default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=localtime())

    important = models.BooleanField(default=False)

    objects = models.Manager()
    pending = PendingManager()

    def is_overdue(self):
        now = localtime()
        return self.end_date < now

    def time_left(self):
        now = localtime()
        return self.end_date - now

    class Meta:
        ordering = ['end_date']
        indexes = [
            models.Index(fields=['end_date'])
        ]

    def __str__(self):
        return self.title
