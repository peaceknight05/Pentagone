# Keras imports
from keras.models import Sequential
from keras.layers import Dense
from keras.metrics import RootMeanSquaredError
from keras.losses import MeanAbsoluteError
from keras.optimizers import Adam

# Create structure
model = Sequential([
    Dense(16, activation="relu", input_shape=(5,)),
    Dense(16, activation="relu"),
    Dense(1, activation="exponential")
])

# Compile
model.compile(optimizer=Adam(learning_rate=0.0011), loss=MeanAbsoluteError(), metrics=[RootMeanSquaredError()])

# Default training data
features = [[1, 0, 0, 0, 1],
            [5, 0, 1, 1, 1],
            [0, 1, 0, 0, -1],
            [0, 5, 0, 0.00833333, -1],
            [3, 0, 0.5, 0.08333333, 1],
            [3, 0, 0.5, 0.5, 1],
            [3, 0, 0.5, 0.04166667, 1],
            [3, 0, 0.08333333, 0.04166667, 1]]

labels = [	1.24814595,
			7.48887569,
			0.01035558,
            0.00517779,
            3.74443784,
            7.48887569,
            3.12036487,
            2.4962919]

# Train on pre-set
model.fit(features, labels, batch_size=2, epochs=5, verbose=0)

# Save
model.save("model.h5")