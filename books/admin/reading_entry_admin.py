from django.contrib import admin
from books.models import ReadingEntry

class ReadingEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'started_at', 'finished_at')
    list_filter = ('status',)


admin.site.register(ReadingEntry, ReadingEntryAdmin)