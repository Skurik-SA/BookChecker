from django.conf import settings
from django.db import models
from django.db.models import JSONField

from books.models import Genre


class Statistics(models.Model):
    user          = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    total_books   = models.PositiveIntegerField(default=0)
    total_pages   = models.PositiveIntegerField(default=0)
    favorite_genre = models.ForeignKey(
        Genre,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    monthly_graph   = JSONField(default=dict, blank=True)
    yearly_graph    = JSONField(default=dict, blank=True)
    updated_at    = models.DateTimeField(auto_now=True)