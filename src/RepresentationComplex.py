# RepresentationComplex.py

import tetris
import constants
import representation
import tensorflow as tf
from representation import Representation
import math

class RepresentationComplex(Representation):
	"""
	A more complex representaion (or feature extraction) of the Tetris game.

	The representation will consist of an array containing:
		column height
		differences in column height
		max column height
		number of holes
		Well depth
	"""

	def __init__(self):
		# column height
		if(constants.REPRESENTATION['col_height']):
			self.col_height = []
			for x in range(constants.HORZBLOCKS):
				self.col_height.append(0)

		# differences in column height
		if(constants.REPRESENTATION['diff_col_height']):
			self.diff_col_height = []
			for x in range(constants.HORZBLOCKS - 1):
				self.diff_col_height.append(0)

		# max column height
		if(constants.REPRESENTATION['max']):
			self.max = 0

		# number of holes
		if(constants.REPRESENTATION['holes']):
			self.holes = constants.VERTBLOCKS * constants.HORZBLOCKS
		
		# well depth
		if(constants.REPRESENTATION['wells']):
			self.wells = []
			for x in range(constants.HORZBLOCKS):
				self.wells.append(0)

	def __str__(self):
		return str([self.col_height, self.diff_col_height, self.max, self.holes, self.wells])

	def clear(self):
		"""Resets the representation"""
		self.__init__()



	def update(self, blk_list):
		"""
		update the representation according to the given block list
		"""
		# set number of holes to be equal to max

		self.holes = constants.VERTBLOCKS * constants.HORZBLOCKS

		for block in blk_list:
			for rect in block.shape:
				x = int((rect.x - 8) / 20)
				y = int(constants.VERTBLOCKS-2-((rect.y - 49) / 20))
				assert((x >= 0 and x <= constants.HORZBLOCKS -1), "Error: x = {}, length of arr = {}".format(x, len(self.col_height)))
				
				#update col_height
				if(constants.REPRESENTATION['col_height']):
					if(x < constants.HORZBLOCKS and self.col_height[x] < y):
						self.col_height[x] = y

				#update diff_col_height
				if(constants.REPRESENTATION['diff_col_height']):
					if(x > 0):
						diff_left = self.col_height[x] - self.col_height[x-1]
						self.diff_col_height[x-1] = diff_left
					if(x < len(self.diff_col_height) - 1):
						diff_right = self.col_height[x] - self.col_height[x+1]
						self.diff_col_height[x+1] = diff_right
					
				#update max column height
				if(constants.REPRESENTATION['max']):
					if(y > self.max):
						self.max = y

				# update number of holes
				if(constants.REPRESENTATION['holes']):
					self.holes -= 1

		if(constants.REPRESENTATION['holes']):
			space_above = constants.VERTBLOCKS * constants.HORZBLOCKS
			for col in self.col_height:
				space_above -= col

			self.holes -= space_above
			assert(self.holes >= 0 and self.holes <= constants.VERTBLOCKS * constants.HORZBLOCKS)


		# update wells
		if(constants.REPRESENTATION['wells']):
			for x in range(len(self.wells)):

				max_x = constants.HORZBLOCKS - 1

				# edge cases
				# left side of the board
				if (x == 0 and self.col_height[x] < self.col_height[x + 1]):
					self.wells[x] = self.col_height[x + 1] - self.col_height[x]
				# right side
				elif(x == max_x and self.col_height[max_x] < self.col_height[max_x - 1]):
					self.wells[x] = self.col_height[x - 1] - self.col_height[x]

				# general case
				elif(x > 0 and x < max_x and self.col_height[x] < self.col_height[x + 1] and self.col_height[x] < self.col_height[x - 1]):
					diff_left = self.col_height[x - 1] - self.col_height[x]
					diff_right = self.col_height[x + 1] - self.col_height[x]
					self.wells[x] = min(diff_left, diff_right)


	def format(self):
		"""
		Returns the formatted version of the representation. So it can be used by tensorflow
		This means that the array is cast to a tf Variable 
		and scaled to a floating point between 0-1
		All features will be concatenated into one array
		"""
		new = []
		if(constants.REPRESENTATION['col_height']):
			for x in range(len(self.col_height)):
				new.append(self.col_height[x] / constants.VERTBLOCKS)

		if(constants.REPRESENTATION['diff_col_height']):
			for x in range(len(self.diff_col_height)):
				new.append(self.diff_col_height[x] / constants.VERTBLOCKS)

		if(constants.REPRESENTATION['max']):
			new.append(self.max / constants.VERTBLOCKS)

		if(constants.REPRESENTATION['holes']):
			holes_formatted = math.log(self.holes + 1) / math.log(constants.VERTBLOCKS * constants.HORZBLOCKS + 1)
			new.append(holes_formatted)

		if(constants.REPRESENTATION['wells']):
			for x in range(len(self.wells)):
				wells_formatted = math.log(self.wells[x] + 1) /  math.log(constants.VERTBLOCKS + 1)
				new.append(wells_formatted)

		for x in new:
			assert((x >= 0 and x <= 1), str(x))

		return tf.Variable([new])



if __name__ == "__main__":
    print("This file is not ment to be ran.\nTry running mlp.py")