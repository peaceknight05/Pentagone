# Pentagone

Pentagone is a web-based tool that improves upon Spaced Repetition Systems (SRS) with continual deep learning. [View the demo video here!](https://drive.google.com/drive/folders/1mt5U07eek9PfkmfKSsUT7AIL48ig5Yja?usp=share_link)

## Brief Introduction to SRS

In essence, SRS is a smarter deck of flashcards, where a system automatically determines when you see a card next, and when you see a new card for the first time, based on how well you recall cards seen.

In practice, you might see a card one time and get it right, then see it again in 5 minutes, then 15, then 30, and so on, as opposed to if you were to get it wrong, you would see it sooner in 1 minute.

The technical aspect of how SRS models the rate at which one forgets something is through the [forgetting curve](https://www.wikiwand.com/en/Forgetting_curve). This curve models the rate at which one retains a piece of information decreases over time at a certain rate determined by the stability constant for that specific piece of information.

Equation for the forgetting curve, where $R$ is the retainability, $t$ is the time elapsed, and $S$ is the stability constant:

$$ R = e^{- \frac{t}{S}} $$

The current system falls short by imposing a single, constant, $S$, for all information and all individuals. Not all information is as easy to learn as another, and not all people learn at the same speed. Thus, the increments in the next review time are fixed and impersonal, which makes it a one-size-fits-all system that does not accommodate people with different learning and retention rates.

## Proposed Improvements

One of the key areas mentioned that the current implementations of SRS are lacking is that the stability constant ($S$ in the equation above) is a fixed value. Our project aims to replace this with a prediction model that can take in parameters (including the longest time retained, last reviewed time, and the number of correct and incorrect recollections) and predict the stability constant for a particular piece of information, factoring in a user's learning ability.

We believe this solves the problem addressed and aids a user to be able to learn better by being able to reinforce their learning just before they forget it.

## Explanation of Code

The repository is split into the front end (which contains all front-facing code), and the back end (which also contains the improved SRS system).

- The front end is powered by [Nuxt](https://nuxtjs.org/), a Vue framework that makes web development simple and powerful. We initially settled for using Django as a front-end framework as well, but considering our lack of technical knowledge about it, we decided to forgo using Django and settle with using something more familiar instead: Vue.
- The back end is powered by [Django](https://www.djangoproject.com/), a robust Python web framework that we mainly use to create a RESTful API accessible to the front end. The API includes endpoints for viewing all decks as well as reviewing a deck.

### Information Stored

The code in `spacedrepetition.py` describes a class `SpacedRepetition`, which contains lists that store the terms to train, their descriptions, and, for each word, the time at which they were last seen, the longest time since last seen where the word was answered correctly, the number of right and wrong answers, the previous time since it was last seen, the previous evaluation, and a cache of predictions for their stability constants. Additionally, to facilitate the continual learning model, it also stores the features (all the information stored with regards to each word) and labels (the stability constant) accumulated to batch-train the model (configurable batch size). The class also keeps track of which predictions require propagation on every training iteration.

In addition to the above information, the threshold that describes the retrievability at which the word/term is considered to be memorised and the "bonus" value (explained later) are also stored.

These are all loaded and saved into a JSON file, save for the configurable parameters, features, labels, and propagation information.

### Step-by-step

The breakdown of how the program fetches the next word is as follows:

1. Get the stability constant of each word (from the cache if possible, otherwise from model prediction)
2. Calculate the retrievability of each word given their stability constants
3. Get the word with the lowest retrievability
   - Low retrievability represents terms most in need of a refresher
   - Retrievability is a measure of how well someone can recall something
4. Get a new word to present to the user
   - Either present the word with the lowest retrievability or a new word if all words are currently memorised (above the threshold)
5. Get from the front-facing code if the user got it right or wrong, update the parameters for that word, accumulate into the training data, and update the cache with the new prediction with the new parameters to save on computation time.
   - If the stored training data is sufficiently large, train the model on the additional data, and propagate changes to the cache of the words that the data was collected from.

> It is worth noting that a standardised timestamp (generated by the server) is used throughout the algorithm to ensure consistent and reliable timekeeping.

### Continual Deep Learning Model

The model is a neural network created with [Keras](https://keras.io/) that has 5 input nodes (number of right, wrong, max time since last seen for a correct answer, time since last seen during latest evaluation, the result of latest evaluation), two hidden layers with 16 nodes each that use Rectified Linear Activation Function (ReLU), and 1 output node that uses an exponential activation function, and gives the predicted stability constant.

The model uses the Adam optimisation algorithm with a learning rate of 0.0011 to ensure that the model can properly increment the intervals while also not increasing too fast and risking a NaN output.

The Mean Absolute Error and Root Mean Squared Error are the metrics used for measuring the loss and evaluation of the model as the model is a regression model at heart.

The code used to set up the model and create the `.h5` file can be found in `generatenetwork.py`. In the code, the fresh model is pre-trained with very little data that teaches it the basic patterns it should know before being used by the user as we have found it to be the best balance between being good to use from the get-go while still being malleable in terms of edge weights so that it can learn to fit each different user.

During each training iteration, it gets trained with additional data collected from the user, which gets labelled by the `calculateStability()` function. To estimate the stability coefficient for each data point, we make use of the relationship between reliability and whether or not the user can recall the information when the cues are presented to them. For a given card that the user gets wrong, we assume the reliability to be around $1 -$ the threshold (by default $1 - 0.8$). For a given card that the user gets right, we assume the reliability to be at least equal to the threshold, $+$ `positiveOffset` (by default $0.8 + 0.11$). `positiveOffset` is a constant that ensures that the intervals get longer at every iteration, as without it, the stability constant will only increase very slowly. This constant models the general principle of how a piece of information is easier to retain every time it gets refreshed in your memory.

> Reminder: the threshold is a constant that represents the retrievability at which we consider a piece of information to still be memorised (i.e. very likely to be able to recall)

The formula that the function `calculateStability()` uses to estimate the stability from the time and outcome is:

$$ S = - \frac{t}{\ln{R}} $$

Where $r$ = `threshold` + `positiveOffset` if the outcome is correct, else it is $1 -$ `threshold`

It is important to note that there is a distinction between how the function estimates the stability constant and how the model predicts the stability constant. The function estimates the stability constant knowing the outcome of whether or not the user can recall it for a given time, while the model predicts the stability constant for a term before it is shown to check if the user can recall it. As such, the two are different in input parameters and use cases, and it cannot be said that the model is simply learning to imitate the function, but rather is forming relationships between the input parameters it is given and the stability constant ascribed by the function.

For demonstration purposes, a `model.h5` file can be found that contains a model that has been put through a good deal of usage.

## Operation

Two languages are used in this project: [Python](https://python.org) and JavaScript ([Node.js](https://nodejs.org/en)). We assume that these languages are already installed in your machine if you wish to run the project locally, and have navigated to the project directory in an appropriate terminal of your choice.

0. (Optionally) create a virtual environment for the back end.

   ```sh
   python3 -m venv .venv
   # Steps may differ for different systems
   source .venv/bin/activate # Linux/UNIX-based shells
   ```

1. Install all dependencies for both the front and back end.

   ```sh
   pip install -r requirements.txt
   ```

   ```sh
   cd frontend && npm install # Feel free to use your own manager of choice (e.g., pnpm, yarn, bun)
   ```

2. Run the back-end server and front-end server.

   ```sh
    cd backend && python3 manage.py runserver
   ```

   ```sh
   cd frontend && npm run dev
   ```

3. Open your preferred browser and navigate to the two opened ports for the back-end (port 8000 by default) and front-end (port 3000 by default) servers.

4. Experiment with the cards and observe how their orderings are made different each time based on the network-predicted stability constant.

Due to time limitations, we couldn't add the functionality to directly edit or create a new deck in the front-end UI. To change or create a wordlist:

0. Read `_template.txt` in `backend/api/data/`, then make a copy of `_template.json` in the same folder.
1. Edit the `words` and `descs` array. Making sure to pad the other arrays with 0s to match the length of the words and descs array.
2. Where needed, `generatenetwork.py` can be used to reset or create a fresh model to re-train.
