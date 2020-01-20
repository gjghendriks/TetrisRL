import random
import csv
import datetime
import tetris
import constants

epochs = 1000

def initialize_writer():
	#init writer

	filename = "outputs/randomagent/"
	filename += datetime.datetime.now().strftime('%c')
	filename += "_output_scores_MLP" 
	filename += ".txt"
	csv_file = open(filename, mode='w')
	print("Writing to file: " + filename)
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
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
				final_score = prev_score
				break
				


			state = random.choice(states)
			board.setState(state)
			board.draw_game()


			prev_score = board.score

		#print("done with one step")
		csv_writer.writerow([final_score])
		print("Training epoch #: {}\t\t Final score = {}".format(epoch, final_score))

	csv_file.close()



if __name__ == "__main__":
    play()