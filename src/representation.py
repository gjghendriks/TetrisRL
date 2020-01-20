# representation.py

import tetris
import constants
import tensorflow as tf

if __name__ == "__main__":
    print("This file is not ment to be run")

class Representation(object):
	"""
	Simple representation of the state of a Tetris board

	Has an array arr with the length equal to the width of the board.
	Each element represents the heigt of each colomn.
	"""

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
		for x in range(len(self.arr)):
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
		Returns the formatted version of the representation. So it can be used by tensorflow
		This means that the array is cast to a tf Variable 
		and scaled to a floating point between 0-1
		"""
		new = []
		for x in range(len(self.arr)):
			new.append(self.arr[x] / 20.0)
		return tf.Variable([new])

