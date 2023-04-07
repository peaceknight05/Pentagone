from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("decks/", views.get_decks, name="decks"),
    path("deck/<str:deck_name>/", views.get_deck, name="deck"),
    path("start_review/", views.start_review, name="start_review"),
    path("review/", views.review, name="review"),
]
