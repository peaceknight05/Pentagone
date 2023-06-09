# Import libraries
import math
import json
from keras.models import load_model

# AI and logic class


class SpacedRepetition:
    name = ""  # Name of deck
    wordlist = []  # Words
    desclist = []  # Descriptions
    timestamps = []  # Timestamp of time last seen (0 if not seen)
    maxtimesince = []  # Longest time since last seen when answered correctly
    lasttimesince = []  # Time since last seen for last iteration
    right, wrong = [], []  # Number of right and wrong answers
    lasteval = []  # Whether last check was right or wrong
    cache = dict()  # Cache predictions to reduce need to re-predict for information that has not changed
    threshold = 0.8  # Threshold for what is considered memorised
    positiveOffset = 0.11  # Reward for getting it right
    n = 0  # Number of cards seen in this session
    batchSize = 10  # Batch size for training
    propagate = []
    features, labels = [], []  # Stored data for training

    # Initalisation function (load from storage)
    def __init__(self, cache, model_path):
        self.name = cache["name"]
        self.wordlist = cache["words"]
        self.desclist = cache["descs"]
        self.timestamps = cache["timestamps"]
        self.maxtimesince = cache["maxtimesince"]
        self.lasttimesince = cache["lasttimesince"]
        self.right = cache["right"]
        self.wrong = cache["wrong"]
        self.lasteval = cache["lasteval"]
        # JSON stores integer keys as strings
        self.cache = {int(k): float(v) for k, v in cache["cache"].items()}
        self.model = load_model(model_path)

    # Currently redundant: add words to wordlist
    def addWords(self, words, descs):
        self.wordlist += words
        self.desclist += descs
        z = [0 for _ in range(len(words))]
        self.timestamps += z
        self.maxtimesince += z
        self.lasttimesince += z
        self.right += z
        self.wrong += z
        self.lasteval += z

    # Dummy model for getting stability constant
    def getPrediction(self, i):
        # Dummy model punishes for wrong answer and rewards
        # For right answers, and increases with maxtimesince
        # return max(-0.0743811837714 * self.wrong[i] + 0.111571775657 * self.right[i] * (1 + self.maxtimesince[i]/120), 0)

        # Use model to predict
        return float(self.model.predict(
            [[self.right[i], self.wrong[i], self.maxtimesince[i] /
                3600, self.lasttimesince[i]/3600, self.lasteval[i]]],
            verbose=0)[0][0])

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
            # Formula for forgetting curve
            return math.e ** (-t / self.getStability(i))
        return 0

    # Get time when retrivability falls
    # Below memorisation threshold.
    def getForgettingTime(self, i):
        t = self.timestamps[i]
        if t == 0:  # If never seen word before
            return 0  # Word is already not memorised
        s = self.getStability(i)
        # Solve for t (converted to seconds) where R = threshold
        # Add to time last seen to get time where R = threshold
        t += -s * math.log(self.threshold) * 3600
        return t

    # Get stability given time and outcome
    # If right, R is taken to be at the threshold
    # If wrong, R is taken to be at 1 - the threshold
    # Solve for S given R and t
    def calculateStability(self, t, outcome):
        return -(t/3600)/math.log(self.threshold+self.positiveOffset if outcome else 1-self.threshold)

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
            # Time for formula is in hours
            timesince = (t - self.timestamps[i])/3600
            r = self.getRetrivability(i, timesince)
            if r < minimum:
                minimum = r
                words[0], words[1], words[2] = i, r, word

        return words

    # Get next word
    def getNext(self, t):
        lowIndex, lowRetrivability, lowWord, newIndex, newWord = self.getLowestAndNew(
            t)
        # If not all words are new, not all words are memorised,
        # Or there are no more new words, show the word with the
        # Lowest retrivability (in most need of a refresher)
        if lowRetrivability != -1 and lowRetrivability < self.threshold:
            return (lowIndex, lowWord, self.desclist[lowIndex], None)
        # Else show a new word to learn
        if newIndex == -1:  # There are no new words to learn and every word is memorised
            # Return next review time
            # (Time when first word will be
            # Below the threshold)
            return (-1, "", "", self.getForgettingTime(lowIndex))
        return (newIndex, newWord, self.desclist[newIndex], None)

    # Train model
    def train(self):
        self.model.fit(
            self.features,
            self.labels,
            batch_size=2,
            epochs=5,
            verbose=0
        )

        # Propagate cache
        for i in self.propagate:
            self.cache[i] = self.getPrediction(i)

    # Process data for training
    def accumulateTrainingData(self, i, correct, t):
        # Set to propagate once training happens
        self.propagate.append(i)
        # Add features and labels
        self.features.append([
            self.right[i],
            self.wrong[i],
            self.maxtimesince[i],
            self.lasttimesince[i],
            self.lasteval[i]])
        self.labels.append(self.calculateStability(t, correct))

    # Retrain model and update statistics
    def review(self, i, correct, t):
        lastseen = self.timestamps[i]
        timesince = t - lastseen if lastseen != 0 else 0
        # Don't train if first time as S will always be calculated as 0
        if timesince != 0:
            self.n += 1
            self.accumulateTrainingData(i, correct, timesince)
        if self.n != 0 and self.n % self.batchSize == 0:
            self.train()
        if correct:
            # If correct increase right count
            # Also update maxtimesince if needed
            self.right[i] += 1
            if timesince > self.maxtimesince[i]:
                self.maxtimesince[i] = timesince
        else:
            # Else update wrong count
            self.wrong[i] += 1
        # Edit last seen timestamp
        self.timestamps[i] = t
        # Update last eval and last time since
        self.lasttimesince[i] = timesince
        self.lasteval[i] = 1 if correct else -1
        # Also update cached information
        self.cache[i] = self.getPrediction(i)

    # Export all stored information
    # (Except for model, which hasn't been
    # Implemented yet)
    def export(self, path, model_path):
        if self.n % self.batchSize != 0:
            self.train()
        json.dump({
            "name": self.name,
            "words": self.wordlist,
            "descs": self.desclist,
            "timestamps": self.timestamps,
            "maxtimesince": self.maxtimesince,
            "lasttimesince": self.lasttimesince,
            "right": self.right,
            "wrong": self.wrong,
            "lasteval": self.lasteval,
            "cache": self.cache
        }, open(path, "w+"), indent=4)
        self.model.save(model_path)
