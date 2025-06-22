
from django.contrib import admin
from books.models import Progress

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['current_page', 'percent', 'entry', 'updated_at']
    search_fields = ['percent']
    list_filter = ['percent']


admin.site.register(Progress, ProgressAdmin)