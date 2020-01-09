import random
import csv
import datetime
import tetris
import constants

epochs = 1000


def play():

	filename = "outputs/randomagent/"
	filename += datetime.datetime.now().strftime('%c')
	filename += "_output_scores_random" 
	filename += ".txt"
	with open(filename, mode='w') as csv_file:
		print("Writing to " + filename)
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for i in range(epochs):
			
			print("Training epoch #: {}".format(i))

			board = tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)

			final_score = 0
			while True:

				states = board.run()

				# nextStates() returns False if the state is invalid (Game over)
				if(not states):
					final_score = prev_score
					break
					


				state = random.choice(states)
				board.setState(state)
				board.draw_board()
				#breakpoint()
				board.detect_line()


				prev_score = board.score

			#print("done with one step")
			csv_writer.writerow([final_score])
			print("Final score = {}".format(final_score))




if __name__ == "__main__":
    play()