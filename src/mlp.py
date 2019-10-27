import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants
import representation as rep
#use for v1 : tf.compat.v1.

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


# init a board
board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)

# init model
model = tf.keras.Sequential([
	tf.keras.layers.Dense(10, input_shape=[constants.HORZBLOCKS,], activation='relu'),
	#tf.keras.layers.Dense(10, activation='relu'),
	tf.keras.layers.Dense(1, activation='linear')
])
#print summary of model
model.summary()

#create model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])


for epoch in range(100):

	'''
	generate all next possible states
	with:
	    blk_list:           list of all the block
	    score:              the current score
	    representation:     the representation of the state
	'''
	states = board.nextStates()
	#init predictions
	predictions = []
	for state in states:

		p = model.predict(state["formatted_representation"])
		predictions.append(p)

	for x in range(len(predictions)):
		print(predictions[x])

	# get the value and index of the largest prediction
	max_value = -float('inf')
	for row_idx, row in enumerate(predictions):    
	    for col_idx, col in enumerate(row):
	        if col > max_value:
	            max_value = col
	            max_index = (row_idx, col_idx)

	print("max = {} index = {}".format(max_value, max_index))
	print(predictions[max_index[0]][max_index[1]])

	board.setState(states[max_index[0]])
	board.draw_board()

print("done")