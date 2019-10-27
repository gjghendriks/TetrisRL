import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants
import representation as rep
#use for v1 : tf.compat.v1.

# init a board
board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
# generate all nest possible states
states = board.nextStates()

print("States generated: {}".format(len(states)))

for x, y in states[0].items():
  print(x, y) 

#placeholder to speed up
"""state = [0,0,0,0,0,0,1,1,2,0]
for n in range(len(state)):
	state[n] = state[n] /20.0

print(state)"""


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
	tf.keras.layers.Dense(10, input_shape=[states[0]["representation"].shape[1]], activation='relu'),
	#tf.keras.layers.Dense(10, activation='relu'),
	tf.keras.layers.Dense(1, activation='softmax')
])

model.summary()


model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])


#shuffle true/false
#train the model
#model.fit(formatted_state, score, batch_size=batch_size, epochs=training_epochs, verbose=2)


predictions = []
for state in states:

	p = model.predict(state["representation"])
	predictions.append(p)

for x in range(len(predictions)):
	print(predictions[x][0])
