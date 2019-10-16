# representation.py

import tetris
import constants

if __name__ == "__main__":
    tetris.Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS).run()

class Representation(object):

	def __init__(self):
		self.arr = []

	def update(self, blocklist):
		for blk in blocklist:
			self.arr = blk.y


	def print(self):
		print(self.arr)


