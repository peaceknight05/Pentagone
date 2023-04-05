from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("decks/", views.DeckListView.as_view(), name="decks"),
    path("deck/<int:pk>/", views.DeckDetailView.as_view(), name="deck"),
]
