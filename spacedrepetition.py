# Import libraries
import math
import json

# AI and logic class
class SpacedRepetition:
	wordlist = [] # Words
	desclist = [] # Descriptions
	timestamps = [] # Timestamp of time last seen (0 if not seen)
	maxtimesince = [] # Longest time since last seen when answered correctly
	right, wrong = [], [] # Number of right and wrong answers
	cache = dict() # Cache predictions to reduce need to re-predict for information that has not changed
	threshold = 0.8 # Threshold for what is considered memorised

	# Initalisation function (load from storage)
	def __init__(self, cache):
		self.wordlist += cache["words"]
		self.desclist += cache["descs"]
		self.timestamps = cache["timestamps"]
		self.maxtimesince = cache["maxtimesince"]
		self.right = cache["right"]
		self.wrong = cache["wrong"]
		self.cache = {int(k):v for k,v in cache["cache"].items()} # JSON stores integer keys as strings
		self.threshold = cache["threshold"]

	# Currently redundant: add words to wordlist
	def addWords(self, words, descs):
		self.wordlist += words
		self.desclist += descs
		z = [0 for _ in range(len(words))]
		self.timestamps += z
		self.maxtimesince += z
		self.right += z
		self.wrong += z

	# Dummy model for getting stability constant
	def getPrediction(self, i):
		# Dummy model punishes for wrong answer and rewards
		# For right answers, and increases with maxtimesince
		return max(-0.0743811837714 * self.wrong[i] + 0.111571775657 * self.right[i] * (1 + self.maxtimesince[i]/120), 0)

	# Get stability constant
	# Uses cached prediction when possible
	# Cache updates on update (right/wrong answer)
	def getStability(self, i):
		if i not in self.cache:
			self.cache[i] = self.getPrediction(i)
		return self.cache[i]

	# Get retrivability value
	# Number from [0, 1]
	# Arbitrary metric for how likely one is to
	# Recall a piece of information after some time, t
	def getRetrivability(self, i, t):
		s = self.getStability(i)
		if s != 0:
			return math.e ** (-t / self.getStability(i)) # Formula for forgetting curve
		return 0

	# Get the word with the lowest retrivability
	# Also gets a new word
	def getLowestAndNew(self, t):
		minimum = 2
		words = [-1, -1, "", -1, ""]
		for i in range(len(self.wordlist)):
			word = self.wordlist[i]
			if self.timestamps[i] == 0:
				if words[3] == -1:
					words[3] = i
					words[4] = word
				continue
			timesince = (t - self.timestamps[i])/3600 # Time for formula is in hours
			if (r:=self.getRetrivability(i, timesince)) < minimum:
				minimum = r
				words[0], words[1], words[2] = i, r, word

		return words

	# Get next word
	def getNext(self, t):
		lowIndex, lowRetrivability, lowWord, newIndex, newWord = self.getLowestAndNew(t)
		# If not all words are new, not all words are memorised,
		# Or there are no more new words, show the word with the
		# Lowest retrivability (in most need of a refresher)
		if lowRetrivability != -1 and lowRetrivability < self.threshold or newIndex == -1:
			return (lowIndex, lowWord, self.desclist[lowIndex])
		# Else show a new word to learn
		return (newIndex, newWord, self.desclist[newIndex])

	# Retrain model and update statistics
	def review(self, i, correct, t):
		if correct:
			# If correct increase right count
			# Also update maxtimesince if needed
			self.right[i] += 1
			lastseen = self.timestamps[i]
			timesince = t - lastseen if lastseen != 0 else 0
			if timesince > self.maxtimesince[i]:
				self.maxtimesince[i] = timesince
		else:
			# Else update wrong count
			self.wrong[i] += 1
		# Edit last seen timestamp
		# Also update cached information
		self.timestamps[i] = t
		self.cache[i] = self.getPrediction(i)

	# Export all stored information
	# (Except for model, which hasn't been
	# Implemented yet)
	def export(self, path):
		json.dump({
			"words": self.wordlist,
			"descs": self.desclist,
			"timestamps": self.timestamps,
			"maxtimesince": self.maxtimesince,
			"right": self.right,
			"wrong": self.wrong,
			"cache": self.cache,
			"prop": self.prop,
			"threshold": self.threshold
		}, open(path, "w+"), indent=4)
