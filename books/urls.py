from django.urls import path

from books.views.book_delete import BookDestroyAPIView
from books.views.book_detail import BookDetailAPIView
from books.views.book_list_create import BookListCreateAPIView
from books.views.note_detail import NoteDetailAPIView
from books.views.note_list_create import NoteListCreateAPIView
from books.views.reading_entry_detail import ReadingEntryDetailAPIView
from books.views.reading_entry_list_create import ReadingEntryListCreateAPIView
from books.views.statistics_retrieve import StatisticsRetrieveAPIView

urlpatterns = [
    # Books API
    path('books/', BookListCreateAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:pk>/delete/', BookDestroyAPIView.as_view(), name='book-detail'),

    # Reading Entries API
    path('entries/', ReadingEntryListCreateAPIView.as_view(), name='entry-list'),
    path('entries/<int:entry_id>/', ReadingEntryDetailAPIView.as_view(), name='entry-detail'),
    path('entries/<int:entry_id>/notes/', NoteListCreateAPIView.as_view(), name='note-list'),
    path('entries/<int:entry_id>/notes/<int:note_id>/', NoteDetailAPIView.as_view(), name='note-detail'),
    
    path('statistics/', StatisticsRetrieveAPIView.as_view(), name='statistics-retrieve'),

]