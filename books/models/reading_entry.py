from django.conf import settings
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
        on_delete=models.CASCADE,
        related_name='reading_entries'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    added_at        = models.DateTimeField(auto_now_add=True)
    started_at      = models.DateField(null=True, blank=True)
    finished_at     = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')  # чтобы не дублировать

    def __str__(self):
        return f'{self.user}: {self.book} ({self.status})'

    def mark_status_by_progress(self):
        prog = getattr(self, 'progress', None)

        if prog and prog.percent >= 100:
            self.status = 'READ'

            # Подставляем дату завершения, если не указана
            if not self.finished_at:
                self.finished_at = prog.updated_at.date()

            self.save(update_fields=['status', 'finished_at'])