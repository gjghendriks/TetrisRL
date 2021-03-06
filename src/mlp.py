import tensorflow as tf
import tetris
import constants
import pygame
import csv
import datetime
import random
import math
import os


# suppress warnings
tf.get_logger().setLevel('ERROR')


def compile_model():
	# init model
	if(constants.REPRESENTATION_COMPLEX):
		model = tf.keras.Sequential([
				tf.keras.layers.Dense(constants.NUM_HIDDEN_NODES, input_shape=[constants.INPUTSHAPE,], activation='sigmoid', use_bias=True, kernel_initializer = 'uniform'),
				tf.keras.layers.Dense(constants.NUM_OUTPUT_NODES, activation='linear', use_bias=True, kernel_initializer='uniform'
				)
		])
	else:
		model = tf.keras.Sequential([
				tf.keras.layers.Dense(constants.NUM_HIDDEN_NODES, input_shape=[constants.HORZBLOCKS,], activation='sigmoid', use_bias=True, kernel_initializer = 'uniform'),
				tf.keras.layers.Dense(constants.NUM_OUTPUT_NODES, activation='linear', use_bias=True, kernel_initializer='uniform'
				)
		])

	model.summary()
	#create model
	model.compile(optimizer=tf.keras.optimizers.Adam(lr=constants.LEARNING_RATE),
		loss='mean_squared_error',
		metrics=['accuracy'])
	tf.keras.utils.plot_model(model, to_file="model.png", show_shapes=True)
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

def initialize_writer():
	"""
	init writer

	The header consists of:
		MLP/RANDOM
		a boolean rep_complex?
		date
	"""
	filename = "outputs/"
	extradir = ""
	if(constants.REPRESENTATION['diff_col_height']):
		extradir += "diff_"
	if(constants.REPRESENTATION['max']):
		extradir += "max_"
	if(constants.REPRESENTATION['holes']):
		extradir += "holes_"
	if(constants.REPRESENTATION['wells']):
		extradir += "wells_"
	if extradir:
		extradir += "/"
	else:
		extradir += "col_height/"
	try:
		os.mkdir("outputs/" + extradir)
	except FileExistsError:
		print("Directory ", extradir, " already exists.")
	filename += extradir

	date = datetime.datetime.now().strftime('%c')
	filename += "MLP_" 
	filename += date
	filename += ".txt"
	csv_file = open(filename, mode='w')
	print("Writing to file: " + filename)
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	header = "MLP" + "_" + str(constants.REPRESENTATION_COMPLEX) + "_" + str(date)
	csv_writer.writerow([header])
	return csv_file, csv_writer


def find_exploration(epoch):
	"""
	Returns the exploration rate for the current epoch.

	The logarithm of base 10 is used. The function maps an input of [0, 1000] to [0.289, 0.031].
	"""
	return ((1/ math.log(epoch + 50, 10)) - 0.3)


def train():

	csv_file, csv_writer = initialize_writer()

	model = compile_model()
	
	if(constants.ENABLE_CAPTURE):
		image_counter = 0
		print("CAPTURE ENABLED")
	if(constants.REPRESENTATION_COMPLEX):
		print("REPRESENTATION_COMPLEX")
	else:
		print("REPRESENTATION_SIMPLE")



	for epoch in range(constants.TRAINING_EPOCHS):
		#init previous prediction
		prev_prediction = None
		# init a new board
		board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
		# init final score
		final_score = 0

		#generate 1000 next states, the model will probably die before that
		for block_number in range(10000):

			#generate next states
			states = board.run()

			# board.run() returns False if the state is invalid (Game over)
			if(not states):
				final_score = prev_score
				print("Training epoch #:{}\tFinal score :\t\t{}".format(epoch,final_score))
				break


			#construct predictions
			predictions = []
			for state in states:
				# for each state predict the expected score
				p = model.predict(state["formatted_representation"])
				predictions.append(p)


			# explore, choose random next state
			if random.random() < find_exploration(epoch):
				choice = random.choice(states)
				board.setState(choice)
				max_value = model.predict(choice['formatted_representation'])[0]
				explored = True

			# not exploring, choose expected best reward
			else:
				explored = False
				max_value, max_index = find_max_index(predictions)
				board.setState(states[max_index[0]])


			board.draw_game()
			if(constants.ENABLE_CAPTURE and epoch > 2980 and image_counter <= 2000):
				image_counter += 1
				pygame.image.save(board.screen, "outputs/screenshots/" + str(image_counter) + ".png")


			'''
			back prop the new prediction
				V(St) = V(St) + alpha*[Rt+1 + gamma * V(St+1) - V(St)]
			which can be rewitten if alpha = 1:
				V(St) = Rt+1 + gamma * V(St+1)
			Where:
				V(St): 		prediction of the previous state 						: prev_prediction
				alpha:		constant step-size parameter/ learning rate 			: constants.Q_LEARNING_RATE
				Rt+1:		Reward of the current state (current score)				: board.score - prev_score
				gamma:		discount rate 											: constants.DISCOUNT_RATE
				V(St+1):	Prediction of the current state 						: max_value
			'''
			# only able to back propagate when t > 0 (after one state)
			if prev_prediction:
				value = (1 - constants.Q_LEARNING_RATE) * prev_prediction + constants.Q_LEARNING_RATE * (board.score - prev_score + constants.DISCOUNT_RATE * max_value)
				model.fit(x=prev_input,y=value,verbose=0)



			#update previous prediction, score and input
			prev_prediction = max_value
			prev_score = board.score
			if explored:
				prev_input = choice['formatted_representation']
			else:
				prev_input = states[max_index[0]]["formatted_representation"]



		# the model has chosen poorly by dying, (DIE MODEL!) back prop negative reward.
		model.fit(x=prev_input, y = [-10], verbose = 0)
		csv_writer.writerow([final_score])

	csv_file.close()
	print("Closing")
	raise SystemExit




def run():
	print("Starting run")
	calc()
	train()
	

def calc():
	constants.INPUTSHAPE = constants.HORZBLOCKS 
	if(constants.REPRESENTATION["diff_col_height"]):
		constants.INPUTSHAPE += constants.HORZBLOCKS - 1
	if(constants.REPRESENTATION["max"]):
		constants.INPUTSHAPE += 1
	if(constants.REPRESENTATION["holes"]):
		constants.INPUTSHAPE += 1
	if(constants.REPRESENTATION["wells"]):
		constants.INPUTSHAPE += constants.HORZBLOCKS
	print(constants.REPRESENTATION)
	print("calculated the inputshape to be:")
	print(constants.INPUTSHAPE)


if __name__ == "__main__":
    run()