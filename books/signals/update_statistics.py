from django.db.models import Count, Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from books.models import ReadingEntry, Genre, Progress
from books.models.statistic import Statistics

from django.db.models.functions import TruncMonth, TruncYear


@receiver([post_save, post_delete], sender=ReadingEntry)
def update_statistics(sender, instance, **kwargs):
    """
    Обновляет статистику пользователя при добавлении, удалении или изменении записи о чтении.
    """
    user = instance.user
    stats, _ = Statistics.objects.get_or_create(user=user)

    done_entries = ReadingEntry.objects.filter(user=user, status='READ')

    # Всего прочитанных книг — количество записей со статусом 'READ'
    stats.total_books = done_entries.count()

    # Всего прочитанных страниц — сумма current_page по всем done_entries
    stats.total_pages = Progress.objects.filter(
        entry__in=done_entries
    ).aggregate(total=Sum('current_page'))['total'] or 0

    # Любимый жанр
    fav = Genre.objects.filter(
        books__reading_entries__in=done_entries
    ).annotate(cnt=Count('books__reading_entries')).order_by('-cnt').first()
    stats.favorite_genre = fav

    # Исключаем записи без finished_at
    finished = done_entries.filter(finished_at__isnull=False)

    # График по месяцам — количество книг завершённых в каждый месяц
    monthly = (
        finished
           .annotate(month=TruncMonth('finished_at'))
           .values('month')
           .annotate(count=Count('id'))
           .order_by('month')
    )
    stats.monthly_graph = {
        item['month'].strftime('%Y-%m'): item['count'] for item in monthly
    }

    # График по годам
    yearly = (
        finished
          .annotate(year=TruncYear('finished_at'))
          .values('year')
          .annotate(count=Count('id'))
          .order_by('year')
    )
    stats.yearly_graph = {
        item['year'].year: item['count'] for item in yearly
    }

    stats.save()