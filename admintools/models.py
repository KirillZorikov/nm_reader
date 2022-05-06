import datetime

from django.db import models
from django.utils import timezone


class CoreModel(models.Model):
    created = models.DateTimeField(
        'Created',
        null=False,
        # default=timezone.now,
        auto_now_add=True,
        editable=False,
    )

    updated = models.DateTimeField(
        'Updated',
        null=False,
        # default=timezone.now,
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True
        ordering = ('-updated',)


    @property
    def is_recently_updated(self):
        return timezone.now() < self.updated + datetime.timedelta(
            seconds=5
        )

    @property
    def is_long_time_updated(self):
        return timezone.now() < self.updated + datetime.timedelta(
            seconds=35
        )