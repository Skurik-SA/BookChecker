from django.db import models

from books.models.reading_entry import ReadingEntry


class Note(models.Model):
    entry = models.ForeignKey(
        ReadingEntry,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    text        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)