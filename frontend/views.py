from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Deck


def index(request):
    return render(request, "index.html")


class DeckListView(ListView):
    model = Deck
    context_object_name = "decks"
    template_name = "decks.html"

    def get_queryset(self):
        return Deck.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["decks"] = Deck.objects.all()
        return context


class DeckDetailView(DetailView):
    model = Deck
    context_object_name = "deck"
    template_name = "deck.html"

    def get_queryset(self):
        return Deck.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = Deck.objects.get(pk=self.kwargs["pk"])
        # Currently, data is in lists of the same size. How can I loop through each list and combine the data for one index into a dictionary?
        context["words"] = [{k: v for k, v in zip(
            ["word", "desc", "timestamp", "maxtimesince", "lasttimesince", "right", "wrong", "lasteval"], inner_list)} for inner_list in list(zip(*context["deck"].data.values()))]
        return context
