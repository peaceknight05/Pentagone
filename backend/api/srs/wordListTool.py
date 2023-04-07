from spacedrepetition import SpacedRepetition

import json
import os

filename = input("name of JSON (without extension): ") + ".json"
if not os.path.exists(filename):
    with open(filename, "w+") as f:
        json.dump({
				"words": [],
				"descs":[],
				"timestamps": [],
				"maxtimesince": [],
				"lasttimesince": [],
                "right": [],
                "wrong": [],
                "lasteval": [],
                "cache": dict()
			}, f)

cache = json.load(open(filename, "r+"))
sr = SpacedRepetition(cache, "model.h5")

words = []
descs = []

n = len(sr.wordlist)
while n:=n+1:
    w = input(f"Word ({n}): ")
    if w == "~": break
    words.append(w)
    descs.append(input("Desc: "))

sr.addWords(words, descs)

sr.export(filename, "model.h5")