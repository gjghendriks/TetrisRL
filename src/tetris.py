#!/usr/bin/env python3

# File: tetris.py 
# Description: Main file with tetris game.

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

import pygame
import pdb
import random
import math
import copy

import block
import constants
if constants.REPRESENTATION_COMPLEX:
    import RepresentationComplex
else:
    import representation

def log(string):
    if constants.DEBUG:
        print(string)


class Tetris(object):
    """
    The class with implementation of tetris game logic.
    """

    def __init__(self,bx,by):
        """
        Initialize the tetris object.

        Parameters:
            - bx - number of blocks in x
            - by - number of blocks in y
        """
        # Compute the resolution of the play board based on the required number of blocks.
        self.resx = bx*constants.BWIDTH+2*constants.BOARD_HEIGHT+constants.BOARD_MARGIN
        self.resy = by*constants.BHEIGHT+2*constants.BOARD_HEIGHT+constants.BOARD_MARGIN
        # Prepare the pygame board objects (white lines)
        self.board_up    = pygame.Rect(0,constants.BOARD_UP_MARGIN,self.resx,constants.BOARD_HEIGHT)
        log(self.board_up)
        self.board_down  = pygame.Rect(0,self.resy-constants.BOARD_HEIGHT,self.resx,constants.BOARD_HEIGHT)
        self.board_left  = pygame.Rect(0,constants.BOARD_UP_MARGIN,constants.BOARD_HEIGHT,self.resy)
        self.board_right = pygame.Rect(self.resx-constants.BOARD_HEIGHT,constants.BOARD_UP_MARGIN-0.5*self.resy,constants.BOARD_HEIGHT,self.resy+ self.resy )
        # List of used blocks
        self.blk_list    = []
        # Compute start indexes for tetris blocks
        self.start_x = math.ceil(self.resx/2.0)
        self.start_y = constants.BOARD_UP_MARGIN + constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        # Blocka data (shapes and colors). The shape is encoded in the list of [X,Y] points. Each point
        # represents the relative position. The true/false value is used for the configuration of rotation where
        # False means no rotate and True allows the rotation.
        self.block_data = (
            ([[0,0],[1,0],[2,0],[3,0]],constants.RED,True),     # I block 
            ([[0,0],[1,0],[0,1],[-1,1]],constants.GREEN,True),  # S block 
            ([[0,0],[1,0],[2,0],[2,1]],constants.BLUE,True),    # J block
            ([[0,0],[0,1],[1,0],[1,1]],constants.ORANGE,False), # O block
            ([[-1,0],[0,0],[0,1],[1,1]],constants.GOLD,True),   # Z block
            ([[0,0],[1,0],[2,0],[1,1]],constants.PURPLE,True),  # T block
            ([[0,0],[1,0],[2,0],[0,1]],constants.CYAN,True),    # L block
        )
        self.letter_data = ["I", "S", "J", "O", "Z", "T", "L"]
        # Compute the number of blocks. When the number of blocks is even, we can use it directly but 
        # we have to decrese the number of blocks in line by one when the number is odd (because of the used margin).
        self.blocks_in_line = bx if bx%2 == 0 else bx-1
        self.blocks_in_pile = by
        # Score settings
        self.score = 0
        # The score level threshold
        self.score_level = constants.SCORE_LEVEL
        self.shape_copy = 0
        self.org_x_copy = 0
        self.org_y_copy = 0
        # Control variables for the game. The done signal is used 
        # to control the main loop (it is set by the quit action), the game_over signal
        # is set by the game logic and it is also used for the detection of "game over" drawing.
        # Finally the new_block variable is used for the requesting of new tetris block. 
        self.done = False
        self.game_over = False
        self.new_block = True
        pygame.font.init()
        self.myfont = pygame.font.SysFont(pygame.font.get_default_font(),constants.FONT_SIZE)
        self.screen = pygame.display.set_mode((self.resx,self.resy))
        pygame.display.set_caption("Tetris")

    def available_rotations(self, letter):
        """
        returns the availble number of rotations
        """
        
        rot = 0

        if(letter == "O"):
            # 1 rotation available
            rot = 1
        elif (letter == "Z" 
            or letter == "S" 
            or letter == "I"):
            #two rotataions available 
            rot = 2
        else:
            # four unique rotations
            rot = 4

        return rot;

    def setState(self, state):
        # sets the state of the board to the argument
        self.score = state['score']
        self.blk_list.clear()
        for blk in state['blk_list']:
            self.blk_list.append(block.Block(copy.deepcopy(blk.shape), blk.x,blk.y,blk.screen,blk.color,blk.rotate_en,blk.letter, True))

    def try_action(self, action):
        """
        Try an action return True if succesful
        If unsuccesful: restore previous state and return False
        """
        # make backup
        self.active_block.backup()
        
        # execute action
        if action == "DOWN":
            self.active_block.move(0,constants.BHEIGHT)
        elif action == "LEFT":
            self.active_block.move(-constants.BWIDTH,0)
        elif action == "RIGHT":
            self.active_block.move(constants.BWIDTH,0)
        elif action == "ROTATE":
            self.active_block.rotate()
        elif action == "PAUSE":
            self.pause()
        else:
            print("INVALID MOVE")

        # if action is not valid, restore
        if(not self.valid_state()):
            self.active_block.restore()
            log("Block restored")
            if constants.DEBUG:
                pygame.time.wait(10)
            return False

        return True

    def valid_state(self):
        '''Returns false if invalid state, returns true otherwise. '''
        down_board  = self.active_block.check_collision([self.board_down])
        any_border  = self.active_block.check_collision([self.board_left,self.board_right])
        top_border  = self.active_block.check_collision([self.board_up])
        block_any   = self.block_colides()
        # Restore the configuration if any collision was detected
        if down_board or any_border or block_any:
            if down_board:
                log("Found a collision with bottom")
            if any_border:
                log("Found a collision with border")
            if block_any:
                log("Found a collision with other block")
            return False
        return True

    def gen_state(self, states):
        """
        Generate the current state as a useable dictonary and save it in the list of states.
        """

        # generate current block list
        new_block_list = []
        for blk in self.blk_list:
            # copy block
            b = block.Block(copy.deepcopy(blk.shape), blk.x, blk.y, blk.screen,blk.color,blk.rotate_en,blk.letter,True)
            new_block_list.append(b)

        #depending on the representation, update it
        if(constants.REPRESENTATION_COMPLEX):
            r = RepresentationComplex.RepresentationComplex()
        else:
            r = representation.Representation()
        r.update(self.blk_list)
        formatted_r = r.format()
        gen_state = {
            "blk_list" : new_block_list,
            "score" : self.score,
            "representation": r,
            "formatted_representation": formatted_r
        }
        states.append(gen_state)


    def generate_all_states(self):
        """
        Generates all states that can come from the current one.
        """

        #initalize list to store states in
        states = []
        # make a copy of the board
        self.backup_board()
        
        # how many rotation are needed?
        rot = self.available_rotations(self.active_block.letter)

        #for every rotation
        for r in range(rot):

            # for every x position 
            # amount of columns - the width
            nmbCols = constants.HORZBLOCKS - self.active_block.get_width() + 1
            for x in range(nmbCols):

                # first move the block all the way to the left
                while(self.try_action("LEFT")):
                    pass

                # move the block to the right x amount of times
                for right in range(x):
                    if not self.try_action("RIGHT"):
                        break

                # try to move the block all the way down
                while(self.try_action("DOWN")):
                    pass


                # final position is found
                # check if a point was scored
                self.detect_line()

                # save the state and reset
                self.gen_state(states)

                # restore to original position
                # reset to the initial state
                self.restore_board()
                

            # try rotate the block
            # if it fails, break from the loop, this won't result in new states
            if not self.try_action("ROTATE"):
                break

            # back up active block, or it doesnt retain rotation
            self.backup_board()


        #return all possible options
        return states

    def run(self):
        '''
        This function makes the board progress one turn or one block.

        returns a list of dicts containing the next possible states from this state
        with:
            blk_list                    : list of all the block
            score                       : the current score
            representation              : the representation of the state
            "formatted_representation"  : the formatted representation
        '''


        # Generate a new block
        log("Getting new block")
        self.new_block = True
        self.get_block()

        #self.draw_game()

        # If the new block spawns in an illegal place, the game is over
        if(not self.valid_state()):
            # the game is over, reset the state
            # remove active block from state
            if self.active_block in self.blk_list:
                self.blk_list.remove(self.active_block)
            return False


        states = self.generate_all_states()
        
        #return the possibilities
        return states

#########################
# Random helper functions
#########################



    def restore_board(self):
        self.blk_list.clear()
        for blk in self.blk_list_cpy:
            restored_block = block.Block(copy.deepcopy(blk.shape),blk.x,blk.y,blk.screen,blk.color,blk.rotate_en,blk.letter, True)
            self.blk_list.append(restored_block)
        self.score = self.score_cpy
        if(not self.blk_list[len(self.blk_list) -1]):
            self.active_block = None
        else:
            self.active_block = self.blk_list[len(self.blk_list) -1]

    def backup_board(self):
        self.blk_list_cpy = []
        for blk in self.blk_list:
            block_copy = block.Block(copy.deepcopy(blk.shape),blk.x,blk.y,blk.screen,blk.color,blk.rotate_en,blk.letter, True)
            self.blk_list_cpy.append(block_copy)
        self.score_cpy = self.score
   
    def print_status_line(self):
        """
        Print the current state line
        """
        string = ["SCORE: {0}".format(self.score)]
        self.print_text(string,constants.POINT_MARGIN,constants.POINT_MARGIN)        

    def print_game_over(self):
        """
        Print the game over string.
        """
        # Print the game over text
        self.print_center(["Game Over","Press \"q\" to exit"])
        # Draw the string
        pygame.display.flip()
        # Wait untill the space is pressed
        while True: 
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.unicode == 'q'):
                    return

    def print_text(self,str_lst,x,y):
        """
        Print the text on the X,Y coordinates. 

        Parameters:
            - str_lst - list of strings to print. Each string is printed on new line.
            - x - X coordinate of the first string
            - y - Y coordinate of the first string
        """
        prev_y = 0
        for string in str_lst:
            size_x,size_y = self.myfont.size(string)
            txt_surf = self.myfont.render(string,False,(255,255,255))
            self.screen.blit(txt_surf,(x,y+prev_y))
            prev_y += size_y 

    def print_center(self,str_list):
        """
        Print the string in the center of the screen.
        
        Parameters:
            - str_lst - list of strings to print. Each string is printed on new line.
        """
        max_xsize = max([tmp[0] for tmp in map(self.myfont.size,str_list)])
        self.print_text(str_list,self.resx/2-max_xsize/2,self.resy/2)

    def block_colides(self):
        """
        Check if the block colides with any other block.

        The function returns True if the collision is detected.
        """
        for blk in self.blk_list:
            # Check if the block is not the same
            if blk == self.active_block:
                continue 
            # Detect situations
            if(blk.check_collision(self.active_block.shape)):
                return True
        return False


    def detect_line(self):
        """
        Detect if the line is filled. If true, returns that line number.
        """
        # Get each shape block of the non-moving tetris block and try
        # to detect the filled line. The number of bulding blocks is passed to the class
        # in the init function.

        #TODO fix this bug whe length is 0
        #could also be when the board is just empty
        if(not len(self.blk_list)):
            print("blklist is empty, is the board empty?")
            pygame.time.wait(1000)
            return

        for block in self.blk_list:
            for shape_block in block.shape:
                tmp_y = shape_block.y
                tmp_cnt = self.get_blocks_in_line(tmp_y)
                assert(tmp_cnt >= 0 and tmp_cnt <= constants.HORZBLOCKS, "tmp_cnt is out of range")
                # Detect if the line contains the given number of blocks
                if tmp_cnt == constants.HORZBLOCKS:
                    # Ok, the full line is detected!
                    # Update the score.
                    self.remove_line(tmp_y)
                    self.score += constants.POINT_VALUE


    def remove_line(self,y):
        """
        Remove the line with given Y coordinates. Blocks below the filled
        line are untouched. The rest of blocks (yi > y) are moved one level done.

        Parameters:
            - y - Y coordinate to remove.
        """ 
        # Iterate over all blocks in the list and remove blocks with the Y coordinate.
        for block in self.blk_list:
            block.remove_blocks(y)
        # Setup new block list (not needed blocks are removed)
        self.blk_list = [blk for blk in self.blk_list if blk.has_blocks()]

    def get_blocks_in_line(self,y):
        """
        Get the number of shape blocks on the Y coordiate.

        Parameters:
            - y - Y coordinate to scan.
        """
        # Iterate over all block's shape list and increment the counter
        # if the shape block equals to the Y coordinate.
        tmp_cnt = 0
        for block in self.blk_list:
            for shape_block in block.shape:
                tmp_cnt += (1 if y == shape_block.y else 0)            
        return tmp_cnt

    def draw_board(self):
        """
        Draw the white board.
        """
        pygame.draw.rect(self.screen,constants.WHITE,self.board_up)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_down)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_left)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_right)
        # Update the score         
        self.print_status_line()

    def get_block(self):
        """
        Generate new block into the game if is required.
        """
        if self.new_block:
            # Get the block and add it into the block list(static for now)
            tmp = random.randint(0,len(self.block_data)-1)
            data = self.block_data[tmp]
            self.active_block = block.Block(data[0],self.start_x,self.start_y,self.screen,data[1],data[2], self.letter_data[tmp], False)
            self.blk_list.append(self.active_block)
            log("generated new block: " + self.active_block.letter + " length = " + str(len(self.blk_list)))
            self.new_block = False

    def draw_game(self):
        """
        Draw the game screen.
        """

        if constants.DISABLE_DRAW:
            return
            
        # Clean the screen, draw the board and draw
        # all tetris blocks
        self.screen.fill(constants.BLACK)
        self.draw_board()
        for blk in self.blk_list:
            blk.draw()
        # Draw the screen buffer
        pygame.display.flip()

if __name__ == "__main__":
    board = Tetris(constants.HORZBLOCKS,constants.VERTBLOCKS)
    board.run()
