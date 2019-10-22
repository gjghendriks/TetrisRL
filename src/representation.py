# representation.py

import tetris
import constants

if __name__ == "__main__":
    tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS).run()

class Representation(object):

	def __init__(self, length):
		self.arr = []
		for x in range(length):
			self.arr.append(0)


	def clear(self):
		"""
		Resets the representation
		"""
		for x in self.arr:
			self.arr[x] = 0


	def add(self, block):
		"""
		add the given block to the representation
		"""
		print(block.shape)
		for rect in block.shape:
			x = int((rect.x - 8) / 20)
			y = int(constants.VERTBLOCKS-2-((rect.y - 49) / 20))
			if(self.arr[x] < y):
				self.arr[x] = y


	def print(self):
		print("Printing representation")
		print(self.arr)


