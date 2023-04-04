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
	currentTime = time.localtime()
	currentTimestamp = time.mktime(currentTime)

	# Get next word from model and diplay
	nextIndex, nextWord, nextDefinition, nextReview = sr.getNext(currentTimestamp)

	# Check if review is needed
	if nextIndex == -1:
		formattedReview = time.strftime("%x %X", time.localtime(nextReview))
		print(f"All words reviewed!\nNext review at: {formattedReview}")
		break

	print(nextDefinition)

	# Get input (word from definition)
	answer = input("> ")

	# Evaluate and train
	if answer == "~": break
	else: sr.review(nextIndex, e:=(answer == nextWord), currentTimestamp)

	# Feedback
	print("Correct!\n" if e else f"Wrong: it was {nextWord}\n")

# Save information
sr.export("cache.json")