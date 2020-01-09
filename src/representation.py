# representation.py

import tetris
import constants
import tensorflow as tf

if __name__ == "__main__":
    tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS).run()

class Representation(object):

	def __init__(self):
		self.arr = []
		for x in range(constants.HORZBLOCKS):
			self.arr.append(0)

	def __str__(self):
		return(str(self.arr))

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
		#print(block.shape)
		for rect in block.shape:
			x = int((rect.x - 8) / 20)
			y = int(constants.VERTBLOCKS-2-((rect.y - 49) / 20))
			if(x < 0 or x > constants.HORZBLOCKS -1):
				breakpoint()
				print("Error: x = {}, length of arr = {}".format(x, len(self.arr)))
				print(rect)
			if(x < 10 and self.arr[x] < y):
				self.arr[x] = y


	def print(self):
		print("Printing representation")
		print(self.arr)


	def format(self):
		"""
		returns the formatted version
		to be used by tensorflow
		"""
		new = []
		for x in range(len(self.arr)):
			new.append(self.arr[x] / 20.0)
		return tf.Variable([new])

