from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from books.models.book import Book


class ReadingEntry(models.Model):
    STATUS_CHOICES  = [
        ('TO_READ', 'Хочу читать'),
        ('READING', 'Читаю сейчас'),
        ('READ', 'Прочитано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    started_at      = models.DateField(null=True, blank=True)
    finished_at     = models.DateField(null=True, blank=True)