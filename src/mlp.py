import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants

#use for v1 : tf.compat.v1.


board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
state = board.nextState()
formatted_state = state.format()
score = [board.score]
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
	tf.keras.layers.Dense(10, input_shape=(10,), activation='relu'),
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


prediction = model.predict(formatted_state)
print(type(prediction))
print(prediction)
