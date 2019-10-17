# representation.py

import tetris
import constants

if __name__ == "__main__":
    tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS).run()

class Representation(object):

	def __init__(self, len):
		self.arr = []
		for x in range(len):
			self.arr.append(0)

	# updates the representation on the basis of the given blocklist
	def update(self, blocklist):
		for shape in blocklist.shape:
				x = int((shape[0] - 8) / 20)
				y = int(constants.VERTBLOCKS-2-((shape[1] - 49) / 20))
				if(self.arr[x] < y):
					self.arr[x] = y


	def print(self):
		print(self.arr)


