
from django.contrib import admin
from books.models import Rating

class RatingAdmin(admin.ModelAdmin):
    list_display = ['score', 'scale']
    search_fields = ['score']


admin.site.register(Rating, RatingAdmin)