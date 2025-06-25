from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='custom_genres'
    )

    def __str__(self):
        return self.name