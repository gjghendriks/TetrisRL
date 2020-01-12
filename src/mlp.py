import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, accuracy_score
import tetris
import constants
import representation as rep
import pygame
import csv
import datetime
import random
#use for v1 : tf.compat.v1.

# defining params
learning_rate = 0.1
training_epochs = 1000
batch_size = 1
display_step = 1
exploration_rate = 0.1
#MLP params
num_input = 10
num_hidden_1 = 10
num_classes = 1

# suppress warnings
tf.get_logger().setLevel('ERROR')




def compile_model():
	# init model
	model = tf.keras.Sequential([
		tf.keras.layers.Dense(10, input_shape=[constants.HORZBLOCKS,], activation=None, use_bias=True),
		tf.keras.layers.Dense(10, activation='sigmoid', use_bias=True),
		tf.keras.layers.Dense(1, activation='linear', use_bias=True,
			#kernel_initializer= tf.keras.initializers.RandomNormal(mean=-0.1, stddev=0.05, seed=None)
			)
	])
	#print summary of model
	model.summary()

	#create model
	model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
		loss='mean_squared_error',
		metrics=['accuracy'])

	return model


def find_max_index(predictions):
	# get the value and index of the largest prediction
	#set the max to -infinity
	max_value = -float('inf')
	for row_idx, row in enumerate(predictions):    
	    for col_idx, col in enumerate(row):
	        if col > max_value:
	            max_value = col
	            max_index = (row_idx, col_idx)

	return max_value, max_index



def train():

	#init writer

	filename = "outputs/mlp/"
	filename += datetime.datetime.now().strftime('%c')
	filename += "_output_scores_MLP" 
	filename += ".txt"
	with open(filename, mode='w') as csv_file:
		print("Writing to file: " + filename)
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


		model = compile_model()


		for i in range(training_epochs):
			weights = model.get_weights()
			#print(weights)
			#init previous prediction
			prev_prediction = None
			# init a new board
			board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
			# init final score
			final_score = 0

			#generate 1000 next states, the model will probably die before that
			for epoch in range(1000):

				'''
				generate all next possible states
				with:
				    blk_list:           		list of all the block
				    score:              		the current score
				    representation:     		the representation of the state
				    formatted_representation: 	the representation that is formatted (normilized and put in an tf.Variable) 
				'''
				states = board.run()

				# nextStates() returns False if the state is invalid (Game over)
				if(not states):
					#pygame.time.wait(100)
					print("Training epoch #:{}\tFinal score :\t\t{}".format(i,final_score))
					final_score = prev_score
					break


				#init predictions
				predictions = []
				for state in states:
					# for each state predict the expected score
					p = model.predict(state["formatted_representation"])
					#save that prediction
					predictions.append(p)
				# explore
				if random.random() < exploration_rate:
					choice = random.choice(states)
					board.setState(choice)
					#breakpoint()
					max_value = model.predict(choice['formatted_representation'])[0]
					eplore = True
					print("explore")
				#normal
				else:
					max_value, max_index = find_max_index(predictions)
					board.setState(states[max_index[0]])

				#print("max = {} index = {}".format(max_value, max_index))
				#print(predictions[max_index[0]][max_index[1]])


				#set the boardstate to the best predicted next state
				board.detect_line()
				board.draw_board()


				'''
				back prop the new prediction
					V(St) = V(St) + alpha*[Rt+1 + gamma * V(St+1) - V(St)]
				Where:
					V(St): 		prediction of the previous state 						: prev_prediction
					alpha:		constant step-size parameter (always 1 in our case)
					Rt+1:		Reward of the current state (current score)				: prev_score - state["score"]
					gamma:		Learning rate 											: constants.DISCOUNT_RATE
					V(St+1):	Prediction of the current state 						: max_value
				'''

				# only able to back propagate when t > 0 (after one state)
				if prev_prediction:
					#print("now backproping")
					value = state["score"]- prev_score + constants.DISCOUNT_RATE * max_value
					#print("value to be backpropagated: {}".format(value))
					#print("Components: prev = {} score = {} score_diff = {} discount_rate = {}, max_value = {} max - prev = {}".format(prev_prediction, state['score'], state["score"] - prev_score, constants.DISCOUNT_RATE, max_value, max_value - prev_prediction))

					#breakpoint()
					model.fit(x=prev_input,
						y=value,
						verbose=0)



				#update previous prediction
				prev_prediction = max_value
				#update previous score
				prev_score = board.score
				#update previous input
				for j in range(len(states)):
					if j == max_index[0]:
						prev_input = states[j]["formatted_representation"]



			#print("done with one epoch")
			csv_writer.writerow([final_score])

if __name__ == "__main__":
    train()