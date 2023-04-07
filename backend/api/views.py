import json
from django.http import JsonResponse
from django.shortcuts import redirect
from .srs.spacedrepetition import SpacedRepetition
from django.views.decorators.csrf import csrf_exempt
import os
import time

CWD = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CWD, "data")
sr = None

def get_file_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)

    # Open the file and load the data.
    with open(file_path, "r") as file:
        json_data = json.load(file)

    return json_data

def index(request):
    return JsonResponse({"message": "This service is working normally.", "status": 200}, status=200)

def get_decks(request):
    decks = []

    # Get all the file names in the data directory.
    count = 0
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json") and not(file in ["_template.json"]):
            data = get_file_data(file)
            decks.append(data)
    
    return JsonResponse({"data": decks, "status": 200}, status=200)
        

def get_deck(request, deck_name):
    # Validates if the deck exists as an existing JSON file.
    file_path = os.path.join(DATA_DIR, deck_name + ".json")
    if not os.path.exists(file_path):
        return JsonResponse({"message": "The deck you requested does not exist.", "status": 404}, status=404)

    data = get_file_data(deck_name + ".json")
    return JsonResponse({"data": data, "status": 200}, status=200)

@csrf_exempt
def start_review(request):
    global sr
    if not request.body or request.body == "":
        return JsonResponse({"message": "You must provide a deck name.", "status": 400}, status=400)

    try:
        deck_name = json.loads(request.body)["deck_name"]
        if not deck_name:
            raise KeyError
    except KeyError:
        return JsonResponse({"message": "You must provide a deck name.", "status": 400}, status=400)
    
    file_path = os.path.join(DATA_DIR, deck_name + ".json")
    if not os.path.exists(file_path):
        return JsonResponse({"message": "The deck you requested does not exist.", "status": 404}, status=404)
    
    sr = SpacedRepetition(get_file_data(file_path), os.path.join(CWD, "srs", "model.h5"))

    # Gets the first word to review.
    currentTimestamp = time.mktime(time.localtime())
    nextIndex, nextWord, nextDefinition, nextReview = sr.getNext(currentTimestamp)

    return JsonResponse({"data": {"deck_name": deck_name, "nextIndex": nextIndex, "nextWord": nextWord, "nextDefinition": nextDefinition, "currentTimestamp": currentTimestamp, "nextReview": nextReview}, "status": 200}, status=200)

@csrf_exempt
def review(request):
    global sr
    if sr is None:
        return JsonResponse({"message": "You must start a review session first.", "status": 400}, status=400)

    try:
        data = json.loads(request.body)
        deck_name = data["deck_name"]
        nextIndex = data["nextIndex"]
        currentTimestamp = data["currentTimestamp"]
        attempt = data["attempt"]
        print(not deck_name, not nextIndex, not currentTimestamp, not (attempt and attempt in ["right", "wrong"]))
        if not deck_name or not currentTimestamp or not (attempt and attempt in ["right", "wrong"]):
            raise KeyError
    except KeyError:
        return JsonResponse({"message": "Expected data payload.", "status": 400}, status=400)

    sr.review(nextIndex, True if attempt == "right" else False, currentTimestamp)

    # Generates the next word to review.
    currentTimestamp = time.mktime(time.localtime())
    nextIndex, nextWord, nextDefinition, nextReview = sr.getNext(currentTimestamp)

    if nextIndex == -1:
        sr.export(os.path.join(DATA_DIR, deck_name + ".json"), os.path.join(CWD, "srs", "model.h5"))
        sr = None
        return JsonResponse({"data": {"nextReview": nextReview}, "message": "You have finished reviewing this deck.", "status": 204}, status=204)

    return JsonResponse({"data": {"deck_name": deck_name, "nextIndex": nextIndex, "nextWord": nextWord, "nextDefinition": nextDefinition, "currentTimestamp": currentTimestamp, "nextReview": nextReview}, "status": 200}, status=200)
