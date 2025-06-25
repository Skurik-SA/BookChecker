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

    def save(self, *args, **kwargs):
        total = self.entry.book.total_pages or 1

        # не больше 100%, не отрицательный
        self.current_page = min(max(self.current_page, 0), total)
        self.percent = round((self.current_page / total) * 100, 1)

        super().save(*args, **kwargs)

        try:
            self.entry.mark_status_by_progress()
        except:
            pass