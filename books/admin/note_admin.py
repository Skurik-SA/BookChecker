
from django.contrib import admin
from books.models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'entry']
    search_fields = ['text']


admin.site.register(Note, NoteAdmin)