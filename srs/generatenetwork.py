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
model.compile(optimizer=Adam(learning_rate=0.01), loss=MeanAbsoluteError(), metrics=[RootMeanSquaredError()])

# Save
model.save("model.h5")