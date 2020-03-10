import pygame
import Quarto
import companionsKQML

class Block:
    def __init__(self, id):
        self.id = id
        
        # self.height = height
        # self.color = color
        # self.solidity = solidity
        # self.shape = shape

"""
    def combine(self, block):
        new_block = Block(False, False, False, False)

        if self.height == block.height:
            new_block.height = self.height
        if self.color == block.color:
            new_block.color = self.color
        if self.solidity == block.solidity:
            new_block.solidity = self.solidity
        if self.shape == block.shape:
            new_block.shape = self.shape

        return new_block

    def check_comb(self):
        if not self.height and not self.color and not self.shape and not self.solidity:
            return False
        return True
"""

class Board:
    def __init__(self):
        spaces = [[0 for i in range(4)] for j in range(4)]
        self.spaces = spaces

    def output(self):
        for i in range(4):
            row = ""
            for j in range(4):
                row = row + self.spaces[i][j]
            print(row)

    def place(self, block, x, y):
        self.spaces[x][y] = block


"""
    def check_whole(self):
        cols = self.check_cols()
        rows = self.check_rows()
        diag = self.check_diag()
        return cols or rows or diag

    def check_cols(self):
        for i in range(4):
            comb_block = self.spaces[i][0].spot
            for j in range(1, 4):
                comb_block = comb_block.combine(self.spaces[i][j].spot)
            if comb_block.check_comb():
                return True
        return False

    def check_rows(self):
        for j in range(4):
            comb_block = self.spaces[0][j].spot
            for i in range(1, 4):
                comb_block = comb_block.combine(self.spaces[i][j].spot)
            if comb_block.check_comb():
                return True
        return False

    def check_diag(self):
        comb_block = self.spaces[0][0].spot
        comb_block = comb_block.combine(self.spaces[1][1].spot)
        comb_block = comb_block.combine(self.spaces[2][2].spot)
        comb_block = comb_block.combine(self.spaces[3][3].spot)
        if comb_block.check_comb():
            return True
        comb_block = self.spaces[0][3].spot
        comb_block = comb_block.combine(self.spaces[1][2].spot)
        comb_block = comb_block.combine(self.spaces[2][1].spot)
        comb_block = comb_block.combine(self.spaces[3][0].spot)
        if comb_block.check_comb():
            return True
        return False


class Space:
    def __init__(self):
        self.spot = Block(False, False, False, False)
"""
def draw_board(screen, on_board, off_board):
    counter = 0
    screen.fill((0,0,0))

    for i in range(4):
        for j in range(4):
            on_board[counter][1].center = (j*100 + 50, i*100 + 50)
            off_board[counter][1].center = (j*75 + 50, i*75 + 500)

            screen.blit(on_board[counter][0], on_board[counter][1])
            screen.blit(off_board[counter][0], off_board[counter][1])

            counter += 1

        pygame.display.flip()

def game():
    """
    unused_pieces = [
        "0000", "0001", "0010", "0011",
        "0100", "0101", "0110", "0111",
        "1000", "1001", "1010", "1011",
        "1100", "1101", "1110", "1111"]
    """

    unused_pieces = []
    for i in range(1,17):
        unused_pieces.append(str(i))

    used_pieces = []

    board = Board()
    #board.output()
    
    # Pygame setup
    pygame.init()
    screen_size = width, height = 600, 800
    screen = pygame.display.set_mode(screen_size)

    # Load images
    empty_tiles = []
    pieces = []

    board_rects = []
    unused_rects = []

    on_board = []
    off_board = []

    for i in range(16):
        # Fill in list of loaded images
        on_board_sprite = pygame.image.load("images/p-1.jpg")
        off_board_sprite = pygame.image.load(("images/p" + str(i+1) + ".jpg"))

        # Create rectangles
        on_board_rect = on_board_sprite.get_rect()
        off_board_rect = off_board_sprite.get_rect()

        on_board.append((on_board_sprite, on_board_rect))
        off_board.append((off_board_sprite, off_board_rect))

    draw_board(screen, on_board, off_board)

    # TODO
    # test_rect = pygame.draw.rect(screen, [255,255,255,128], )

    # Backend magic
    quarto_agent = Quarto.QuartoAgent.parse_command_line_args()
    Quarto.resetBoard(quarto_agent)

    ai_set = False
    while not ai_set:
        ai_set = True
        ai_strat = input("Select AI strategy. S for Survivor, D for Denier, C for Complicator.  >>")
        if ai_strat == "S":
            ai_strat = "Survivor"
        elif ai_strat == "D":
            ai_strat = "Denier"
        elif ai_strat == "C":
            ai_strat = "Complicator"
        else: 
            print("Invalid AI type")
            ai_set = False

    Quarto.setPlayerType(quarto_agent, ai_strat)

    computer_places = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Get piece from user
        if computer_places:
            input_block = input("Please enter piece: ")

            # Check if piece is legal
            if input_block in used_pieces:
                print("Piece has already been used!")

            elif input_block not in unused_pieces:
                print("Not a legal piece!")

            else:
                # Get placement from computer
                # Update backend gamestate
                givePieceHuman(quarto_agent, input_block)
                # Ask for where it placed it
                ai_result = getBoard(quarto_agent)

                for cell in ai_result:
                    cell_x = Quarto.convert_to_int(cell[1])-1
                    cell_y = Quarto.convert_to_int(cell[2])-1
                    piece_id = str(cell[3]).strip("piece")
                    
                    if piece_id != "Empty" and board.spaces[cell_x][cell_y] == 0:
                        input_x = cell_x
                        input_y = cell_y
                        break
                
                # Check if coordinate is legal
                # input_x = int(input("Please enter x: "))
                # input_y = int(input("Please enter y: "))

                if input_x < 0 or input_x > 3 or input_y < 0 or input_y > 3:
                    print("Index out of range!")

                elif board.spaces[input_x][input_y] != 0:
                    print("A piece has already been placed there!")

                else:
                    # Place piece
                    board.place(Block(input_block), int(input_x), int(input_y))
                    
                    # Swap piece off board with empty tile on board
                    list_index = input_x + (input_y * 4)
                    swap_out = on_board[list_index]
                    on_board[list_index] = off_board[int(input_block)-1]
                    off_board[int(input_block)-1] = swap_out

                    draw_board(screen, on_board, off_board)

                    used_pieces.append(input_block)
                    idx_to_delete = unused_pieces.index(input_block)
                    del unused_pieces[idx_to_delete]

        else:
            # Get piece from computer
            input_block = Quarto.givenPiece(quarto_agent).strip("piece")

            if input_block in used_pieces:
                print("Piece has already been used!")

            elif input_block not in unused_pieces:
                print("Not a legal piece!")

            else:
                input_x = int(input("Please enter x: "))
                input_y = int(input("Please enter y: "))

                # Check if coordinate is legal
                if input_x < 0 or input_x > 3 or input_y < 0 or input_y > 3:
                    print("Index out of range!")

                elif board.spaces[input_x][input_y] != 0:
                    print("A piece has already been placed there!")

                else:
                    # Place piece
                    board.place(Block(input_block), int(input_x), int(input_y))
                    Quarto.placePieceHuman(quarto_agent, input_x+1, input_y+1)
                    
                    # Swap piece off board with empty tile on board
                    list_index = input_x + (input_y * 4)
                    swap_out = on_board[list_index]
                    on_board[list_index] = off_board[int(input_block)-1]
                    off_board[int(input_block)-1] = swap_out

                    draw_board(screen, on_board, off_board)

                    used_pieces.append(input_block)
                    idx_to_delete = unused_pieces.index(input_block)
                    del unused_pieces[idx_to_delete]

        computer_places = not computer_places

        """
        if board.check_whole():
            print("QUARTO!")
        """


if __name__ == "__main__":
    game()