
from django.contrib import admin
from books.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'total_pages', 'cover']
    search_fields = ['title', 'author']
    list_filter = ['genres']
    filter_horizontal = ['genres']


admin.site.register(Book, BookAdmin)