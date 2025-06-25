# books/admin.py

from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.forms import Textarea
from django.utils.html import format_html

from books.models.statistic import Statistics
from books.signals import update_statistics


class StatisticsAdminForm(forms.ModelForm):
    class Meta:
        model = Statistics
        fields = '__all__'
        widgets = {
            # если у вас PostgreSQL, можно показывать JSON в виде читаемого textarea
            'monthly_graph': Textarea(attrs={'rows': 6, 'cols': 40}),
            'yearly_graph':  Textarea(attrs={'rows': 6, 'cols': 40}),
        }


class StatisticsAdmin(admin.ModelAdmin):
    form = StatisticsAdminForm

    list_display = (
        'user',
        'total_books',
        'total_pages',
        'favorite_genre',
        'updated_at',
        'view_monthly_graph',
    )
    list_select_related = ('user', 'favorite_genre')
    raw_id_fields      = ('user', 'favorite_genre')
    list_filter        = ('favorite_genre', 'updated_at')
    search_fields      = ('user__email', 'user__username')
    readonly_fields    = (
        'total_books',
        'total_pages',
        'favorite_genre',
        'updated_at',
        'monthly_graph',
        'yearly_graph',
    )
    ordering = ('-updated_at',)

    fieldsets = (
        (None, {
            'fields': ('user',),
        }),
        ('Aggregated Data', {
            'fields': (
                'total_books',
                'total_pages',
                'favorite_genre',
                'updated_at',
            ),
            'description': 'Эти поля автоматически пересчитываются сигналами при изменениях ReadingEntry',
        }),
        ('Graphs (JSON)', {
            'fields': ('monthly_graph', 'yearly_graph'),
            'description': 'Количество прочитанных книг по месяцам и годам в формате JSON',
        }),
    )

    actions = ['recalculate_statistics']

    def view_monthly_graph(self, obj):
        """
        Показываем краткую HTML-таблицу по monthly_graph прямо в списке.
        """
        if not obj.monthly_graph:
            return "-"
        rows = "".join(
            f"<tr><td>{month}</td><td>{count}</td></tr>"
            for month, count in obj.monthly_graph.items()
        )
        html = f"<table style='border-collapse: collapse;'><thead><th>Месяц</th><th>Книг</th></thead><tbody>{rows}</tbody></table>"
        return format_html(html)
    view_monthly_graph.short_description = "По месяцам"

    def recalculate_statistics(self, request, queryset):
        """
        Админ-экшен: заново прогнать сигнал update_statistics для
        выбранных объектов.
        """
        for stats in queryset:
            # вручную обновляем статистику
            # вызываем нашу функцию-сигнал, передаём ReadingEntry в качестве sender
            update_statistics(sender=None, instance=stats.user.statistics)
        self.message_user(request, "Статистика пересчитана для выделенных записей.")
    recalculate_statistics.short_description = "Пересчитать статистику"


admin.site.register(Statistics, StatisticsAdmin)