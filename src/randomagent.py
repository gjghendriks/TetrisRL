import random
import csv
import datetime
import tetris
import constants

epochs = 1000

def initialize_writer():
	"""
	init writer

	The header consists of:
		MLP/RANDOM
		a boolean rep_complex?
		date
	"""

	filename = "outputs/randomagent/"
	date = datetime.datetime.now().strftime('%c')
	filename += "RANDOM_" 
	filename += date
	filename += ".txt"
	csv_file = open(filename, mode='w')
	print("Writing to file: " + filename)
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	header = "RANDOM" + "_" + str(constants.REPRESENTATION_COMPLEX) + "_" + str(date)
	csv_writer.writerow([header])
	return csv_file, csv_writer




def play():

	csv_file, csv_writer = initialize_writer()

	for epoch in range(epochs):
		

		board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
		final_score = 0
		while True:

			states = board.run()

			# board.run() returns False if the state is invalid (Game over)
			if(not states):
				break
				


			state = random.choice(states)
			board.setState(state)
			board.draw_game()


			final_score = board.score

		csv_writer.writerow([final_score])
		print("Training epoch #: {}\t\t Final score = {}".format(epoch, final_score))

	csv_file.close()



if __name__ == "__main__":
    play()