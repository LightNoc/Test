from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView

from catalog.models import Game
# Create your views here.
from .models import Book, Author, BookInstance, Genre, Game

def index(request):
    """View function for home page of site."""

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class GameListView(ListView):
    model = Game
    template_name = 'games.html'
    context_object_name = 'games'
    paginate_by = 30  # Set the number of results per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_list = self.get_queryset()

        # Add pagination to the context
        paginator = Paginator(game_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            games = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            games = paginator.page(paginator.num_pages)

        context['games'] = games
        return context
