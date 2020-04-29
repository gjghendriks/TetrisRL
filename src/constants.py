#!/usr/bin/env python3

# File: constants.py 
# Description: Basic program constants.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pygame.locals import *


# Hyper parameters
NUM_HIDDEN_NODES = 50
NUM_OUTPUT_NODES = 1
TRAINING_EPOCHS = 3000
DISCOUNT_RATE = 0.95
LEARNING_RATE = 0.0001
Q_LEARNING_RATE = 1

# representation complex or simple
REPRESENTATION_COMPLEX = True

REPRESENTATION = {
	"col_height" : True,
	"diff_col_height" : True,
	"max" : True,
	"holes" : True,
	"wells": True
}

#Disale the draw function to speed up the training
DISABLE_DRAW = False

# Enable/disable the capuring of screenshot for every step of a game.
# Can't be true if disable draw is true
ENABLE_CAPTURE = False
assert((not ENABLE_CAPTURE) or (not DISABLE_DRAW))

# number of blocks that the game can fit vertically
VERTBLOCKS = 20
# number of block that the game can fit horizontally
HORZBLOCKS = 10

# input shape consist of an array containing:
		#	column height
		#	differences in column height
		#	max column height
		#	number of holes
		#	Well depth


DEBUG = False


INPUTSHAPE = HORZBLOCKS 
if(REPRESENTATION["diff_col_height"]):
	INPUTSHAPE += HORZBLOCKS - 1
if(REPRESENTATION["max"]):
	INPUTSHAPE += 1
if(REPRESENTATION["holes"]):
	INPUTSHAPE += 1
if(REPRESENTATION["wells"]):
	INPUTSHAPE += HORZBLOCKS

#####################
#### DONT CHANGE ####

# Configuration of building shape block
# Width of the shape block
BWIDTH     = 20
# Height of the shape block
BHEIGHT    = 20
# Width of the line around the block
MESH_WIDTH = 1

# Configuration of the player board
# Board line height
BOARD_HEIGHT     = 7
# Margin of upper line (for score)
BOARD_UP_MARGIN  = 40
# Margins around all lines
BOARD_MARGIN     = 2

# Color declarations in the RGB notation
WHITE    = (255,255,255)
RED      = (255,0,0)
GREEN    = (0,255,0)
BLUE     = (0,0,255)
ORANGE   = (255,69,0)
GOLD     = (255,125,0)
PURPLE   = (128,0,128)
CYAN     = (0,255,255) 
BLACK    = (0,0,0)

# Timing constraints
# Time for the generation of TIME_MOVE_EVENT (ms)
MOVE_TICK          = 1000
# Allocated number for the move dowon event
TIMER_MOVE_EVENT   = USEREVENT+1
# Speed up ratio of the game (integer values)
GAME_SPEEDUP_RATIO = 1.5
# Score LEVEL - first threshold of the score
SCORE_LEVEL        = 2000
# Score level ratio
SCORE_LEVEL_RATIO  = 2 

# Configuration of score
# Number of points for one building block
POINT_VALUE       = 1
# Margin of the SCORE string
POINT_MARGIN      = 10

# Font size for all strings (score, pause, game over)
FONT_SIZE           = 25
