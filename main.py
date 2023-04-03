# Import SRS AI
from spacedrepetition import SpacedRepetition

# Import libraries
import json
import time

# Load stored information and instantiate
cache = json.load(open("cache.json", "r+"))
sr = SpacedRepetition(cache)

# Event loop
while 1:
	# Get current time to standardise operations
	currentTime = time.time()

	# Get next word from model and diplay
	nextIndex, nextWord, nextDefinition = sr.getNext(currentTime)
	print(nextDefinition)

	# Get input (word from definition)
	answer = input("> ")

	# Evaluate and train
	if answer == "~": break
	else: sr.review(nextIndex, e:=(answer == nextWord), currentTime)

	# Feedback
	print("Correct!\n" if e else f"Wrong: it was {nextWord}\n")

# Save information
sr.export("cache.json")