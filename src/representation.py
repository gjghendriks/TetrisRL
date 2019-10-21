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

	def clear(self):
		self.arr.clear()

	# add to the representation on the basis of the given blocklist
	def add(self, block):
		print(block.shape)
		for rect in block.shape:
			x = int((rect.x - 8) / 20)
			y = int(constants.VERTBLOCKS-2-((rect.y - 49) / 20))
			print("x = ")
			print(x)
			print(rect.x)
			if(self.arr[x] < y):
				self.arr[x] = y


	def print(self):
		print("Printing representation")
		print(self.arr)


