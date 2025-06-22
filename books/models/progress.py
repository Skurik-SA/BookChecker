from django.db import models

from books.models.reading_entry import ReadingEntry


class Progress(models.Model):
    entry = models.OneToOneField(
        ReadingEntry,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    current_page    = models.PositiveIntegerField(default=0)
    percent         = models.FloatField(default=0.0)
    updated_at      = models.DateTimeField(auto_now=True)