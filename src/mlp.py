import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants

#use for v1 : tf.compat.v1.


board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
state = board.nextState()
formatted_state = state.format()
#placeholder to speed up
"""state = [0,0,0,0,0,0,1,1,2,0]
for n in range(len(state)):
	state[n] = state[n] /20.0

print(state)"""
#s = tf.compat.v1.InteractiveSession()


# defining params
learning_rate = 0.001
training_epochs = 15
batch_size = 1
display_step = 1
regularizer_rate = 0.1
#MLP params
num_input = 10
num_hidden_1 = 10
num_classes = 1


model = tf.keras.Sequential([
	tf.keras.layers.Flatten(input_shape=(10, 1)),
	tf.keras.layers.Dense(10, activation='relu'),
	tf.keras.layers.Dense(1, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])

print("hello")
print(model.weights)