from django.db import models

from books.models.reading_entry import ReadingEntry


class Rating(models.Model):
    entry = models.OneToOneField(
        ReadingEntry,
        on_delete=models.CASCADE,
        related_name='rating'
    )

    score           = models.PositiveSmallIntegerField()
    SCALE_CHOICES   = [(5, '5-балльная'), (10, '10-балльная')]
    scale           = models.IntegerField(choices=SCALE_CHOICES, default=5)