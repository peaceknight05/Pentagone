# Pentagone

Proof-of-concept project to show how a Machine Learning model can be applied to a Spaced Repetition System (SRS) learning method.

## Brief Introduction to SRS

SRS essentially is a smarter deck of flashcards, where a system automatically determines when you see a card next, and when you see a new card for the first time, based on how well you recall cards seen.

In practice, you might see a card one time and get it right, then see it again in 5 minutes, in 15, in 30, and so on. As opposed to if you were to get it wrong, you would see it sooner in 1 minute.

The technical aspect about how SRS models the rate at which one forgets something is through the [forgetting curve](https://www.wikiwand.com/en/Forgetting_curve). This curve models the rate at which one retains a piece of information decreases over time at a certain rate determined by the stability constant for that specific piece of information.

Equation for the forgetting curve, where R is the retainability, t is the time elapsed, and S is the stability constant:
$$ R = e^{- \frac{t}{S}} $$

The current system falls short by imposing a single, constant, S for all information, for all individuals, when not all information is as easy to learn as the other, and not all people learn at the same speeds. Thus, the increments in the next review time is fixed and impersonal, which makes it a one-size-fits-all system that does not accommodate to people with different learning and retention rates.

## Proposed Improvements

As mentioned, one of the key areas that the current implementations of SRS are lacking is that the stability constant (S in the equation above), is a figure set in stone. Our project will aim to replace this with a prediction model, that is able to take in parameters (to be determined), and predict the stability constant for a particular piece of information, given how the individual has been performing.

This will solve the problem addressed, and hence aid the individual to be able to learn better by better being able to reinforce their learning just before they forget it.

## Explanation of Current Proof of Concept

The repository contains two files. `main.py`, which contains all the front-facing code (the bare-bones interface), and `spacedrepetition.py`. The former is a trivial piece of code that simply fetches the next word and tells the model if the user has gotten it right and wrong, as well as providing a standardised time to use for timekeeping. As such, this document will only go into detail with regards to the inner workings of the latter piece of code.

### Information Stored

The code describes a class `SpacedRepetition`, which contains arrays that store the words/terms to train, their descriptions, and for each word: the time at which they were last seen, the longest time since last seen where the word was answered correctly, the number of right and wrong answers, and a cache of predictions for their stability constants.

Additionally, the threshold that describes the retrivability at which the word/term is considered to be memorised is also stored.

These information are all loaded and saved into a JSON file, although it currently does not include the model information, given that it has not been implemented.

### Step-by-step

The breakdown of how the program fetches the next word is as follows:

- Get the stability constant of each word (from the cache if possible, otherwise from model prediction)
- Calculate the retrivability of each word given their stability constant
- Get the word with the lowest retrivability
  - Low retrivability represents most in need of a refresher
  - Retrivability is a measure of how well someone is able to recall something
- Also get a new word to present to the user
- Either present the word with the lowest retrivability, or a new word, if all words are currently memorised (above the threshold)
- Get from the front-facing code if the user got it right or wrong, update the parameters for that word, update the model, re-predict the stability constant, and save in cache to save on computation time.

#### Dummy model

The program currently uses a dummy model to predict the stability constant which will eventually be sunsetted in favour of a machine learning model. As such, it's not of great importance to fully understand it, although it would be useful to understand what our model might also emulate.

It currently works by increasing the constant for every right answer (with a weightage that increases for a higher maximum time since las seen), and decreases the constant for every wrong answer.

The weightages for right and wrong answers are arbitrarily picked by solving the equation of the forggeting curve for an expected decline of retrivability after a certain time.

The equation in question:

$$ \max(- \frac{20}{60} \ln T \cdot W + \frac{30}{60} \ln T \cdot R \cdot (1 + M/120), 0) $$

Where T is the threshold (hardcoded to assume 0.8), W and R are the number of wrong and right answers for that word/term respectively, and M is the max time since last seen for a right answer in seconds.

## Operation of the Code

To start, simply run `main.py` in python (>=3.10.0). You will be prompted with the description of the word/term, and you just have to answer with the word/term (input is not sanitised, so it is case and punctuation sensitive). To exit the loop, type `~` as your answer. You must not exit with a KeyboardInterrupt or it will not save your progress.

To change the wordlist, edit the words and descs array in `cache.json`, making sure to pad the three other arrays with 0s to match the length of the words and descs array. Alternatively, to "reset" it, copy and paste the contents of the `blankslate.json` file into `cache.json`.

In the JSON file, you can also change the threshold of when you are considered to have memorised something (although the dummy model's coefficients will not update).
