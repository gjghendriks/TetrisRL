import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants
import representation as rep
import pygame
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


def train():



	# init model
	model = tf.keras.Sequential([
		tf.keras.layers.Dense(10, input_shape=[constants.HORZBLOCKS,], activation='relu'),
		#tf.keras.layers.Dense(10, activation='relu'),
		tf.keras.layers.Dense(1, activation='linear', kernel_initializer= tf.keras.initializers.RandomNormal(mean=-0.1, stddev=0.05, seed=None))
	])
	#print summary of model
	model.summary()

	#create model
	model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])




	for i in range(training_epochs):
		#init previous prediction
		prev_prediction = None
		# init a new board
		board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)


		#generate 100 next states, the model will probably die before that
		for epoch in range(1000):

			'''
			generate all next possible states
			with:
			    blk_list:           		list of all the block
			    score:              		the current score
			    representation:     		the representation of the state
			    formatted_representation: 	the representation that is formatted (normilized and put in an tf.Variable) 
			'''
			states = board.nextStates()

			# nextStates() returns False if the state is invalid (Game over)
			if(not states):
				break

			#init predictions
			predictions = []
			for state in states:
				# for each state predict the expected score
				p = model.predict(state["formatted_representation"])
				#save that prediction
				predictions.append(p)


			# get the value and index of the largest prediction
			#set the max to -infinity
			max_value = -float('inf')
			for row_idx, row in enumerate(predictions):    
			    for col_idx, col in enumerate(row):
			        if col > max_value:
			            max_value = col
			            max_index = (row_idx, col_idx)

			print("max = {} index = {}".format(max_value, max_index))
			print(predictions[max_index[0]][max_index[1]])


			#set the boardstate to the best predicted next state
			board.setState(states[max_index[0]])
			board.draw_board()


			'''
			back prop the new prediction
				V(St) = V(St) + alpha*[Rt+1 + gamma * V(St+1) - V(St)]
			Where:
				V(St): 		prediction of the previous state 						: prev_prediction
				alpha:		constant step-size parameter (always 1 in our case)
				Rt+1:		Reward of the current state (current score)				: prev_score - state["score"]
				gamma:		Learning rate 											: discount_rate
				V(St+1):	Prediction of the current state 						: max_value
			'''

			# only able to back propagate when t > 0 (after one state)
			if prev_prediction:
				print("now backproping")
				value = prev_prediction + state["score"]- prev_score + constants.DISCOUNT_RATE * (max_value - prev_prediction)
				print("value to be backpropagated: {}".format(value))
				print("Components: prev = {} score = {} score_diff = {} discount_rate = {}, max_value = {} max - prev = {}".format(prev_prediction, state['score'], state["score"] - prev_score, constants.DISCOUNT_RATE, max_value, max_value - prev_prediction))


				model.fit(x=prev_input,
					y=value,
					verbose=2)



			#update previous prediction
			prev_prediction = max_value
			#update previous score
			prev_score = state["score"]
			#update previous input
			for i in range(len(states)):
				if i == max_index[0]:
					prev_input = states[i]["formatted_representation"]



		print("done with one epoch")




if __name__ == "__main__":
    train()