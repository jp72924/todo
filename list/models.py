from django.db import models


class PriotityManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(important=True)


class Task(models.Model):

    class Status(models.TextChoices):
        SUCESS = 'success', 'Success'
        PENDING = 'pending', 'Pending'

    title = models.CharField(max_length=80)
    descrip = models.CharField('description', max_length=280)
    status = models.CharField(max_length=7,
        choices=Status.choices,
        default=Status.PENDING)

    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    important = models.BooleanField(default=False)

    objects = models.Manager()
    priority = PriotityManager()

    class Meta:
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['-due_date'])
        ]

    def __str__(self):
        return self.title
