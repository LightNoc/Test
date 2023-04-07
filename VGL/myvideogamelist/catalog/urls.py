from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
