import pygame
import time
import sys

# Set Vars
SPACE = 10
SCREEN_SIZE = 600
RECT_SIZE = SCREEN_SIZE / 3 - SPACE*2
RECT_AMNT = 3*3

X_SIZE = RECT_SIZE / 2 - SPACE

GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

NO_PLAYER = 0
PLAYER_1 = 1
PLAYER_2 = 2

# solutions
SOLUTIONS = [
    #-- Row win
    [True, True, True, False, False, False, False, False, False],
    [False, False, False, True, True, True, False, False, False],
    [False, False, False, False, False, False, True, True, True],
    #-- Colum win
    [True, False, False, True, False, False, True, False, False],
    [False, True, False, False, True, False, False, True, False],
    [False, False, True, False, False, True, False, False, True],
    #-- Diagial win
    [True, False, False, False, True, False, False, False, True],
    [False, False, True, False, True, False, True, False, False]
]

class GameLoop:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tic Tac Toe')
        self.win = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))

        # Objects
        self.rects = []
        self.board = []
        self.x_obj = []
        self.o_obj = []

        # player control
        # Player 1 is X True
        # Player 2 is O False
        self.turnWho = True

        self.create_rect()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.isGameComplete():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        for i,item in enumerate(self.rects):
                            if item[0].get_rect(topleft=(item[1],item[2])).collidepoint(mouse_pos):
                                grid_coords = self.rect_coords(i)
                                self.player_handle(grid_coords, item, i)
                else:
                    self.gameComplete()

            self.win.fill(GRAY)
            for x in self.x_obj:
                x.draw()
            self.display_rects()
            for o in self.o_obj:
                o.draw()

            # Update the display
            pygame.display.flip()

    def create_rect(self):
        for i in range(3):
            for j in range(3):
                rect = pygame.Surface((RECT_SIZE,RECT_SIZE))
                y = RECT_SIZE * i*1.1 + SPACE
                x = RECT_SIZE * j*1.1 + SPACE
                rect.fill(WHITE)

                self.rects.append([rect,x,y,NO_PLAYER])

    def display_rects(self):
        for item in self.rects:
            self.win.blit(item[0], (item[1], item[2]))

    def rect_coords(self,index):
        if index <= 2:
            y = 0
            x = index
        elif index >= 3 and index <= 5:
            y = 1
            x = index - 3
        elif index > 5:
            y = 2
            x = index - 6
        return (x,y)

    def player_handle(self,coords,rect,rect_index):
        if self.rectAlreadyClicked(coords):
            # print(f"{coords} Already selected")
            return
        if self.turnWho: # X
            self.turnWho = False
            self.x_obj.append(X_Obj(rect[1],rect[2],coords, rect[0]))
            self.rects[rect_index][-1] = PLAYER_1
        elif not self.turnWho: # O
            self.turnWho = True
            self.o_obj.append(O_Obj(rect[1],rect[2],coords, rect[0]))
            self.rects[rect_index][-1] = PLAYER_2

    def rectAlreadyClicked(self,coords):
        for x in self.x_obj:
            if x.coords == coords:
                return True
        for o in self.o_obj:
            if o.coords == coords:
                return True
        return False

    def gameComplete(self):
        self.getBoard()
        result = self.checkWin()
        if result == PLAYER_1:
            print("---X WON---")
            return True
        elif result == PLAYER_2:
            print("---O WON---")
            return True
        return False

    def getBoard(self):
        self.board.clear()
        for item in self.rects:
            self.board.append(item[-1])
        # print(self.board)

    def checkWin(self):
        board1 = self.configureBoard(PLAYER_1)
        board2 = self.configureBoard(PLAYER_2)
        # for player in range(2) + 1:
        if self.compareSolutionWithBoard(board1):
            return PLAYER_1
        if self.compareSolutionWithBoard(board2):
            return PLAYER_2
        return NO_PLAYER

    def compareSolutionWithBoard(self,board):
        result_board = []
        for solution in SOLUTIONS:
            for index, check in enumerate(solution):
                if check and board[index]:
                    result_board.append(True)
            if len(result_board) == 3:
                return True
            else:
                result_board.clear()

        return False

    def configureBoard(self,player):
        board = []
        for rect in self.board:
            if rect == player:
                board.append(True)
            else:
                board.append(False)
        # print(board)
        return board

    def isGameComplete(self):
        counter = 0
        for item in self.rects:
            if item[-1] > 0:
                counter+=1
        if counter == 9:
            print("---No ONE WON--")
            return True
        if self.gameComplete():
            return True
        return False

class Objects:
    def __init__(self, x, y, coords, surface):
        self.x = x
        self.y = y
        self.surface = surface
        self.coords = coords # row and col in grid

class X_Obj(Objects):
    def __init__(self, x, y, coords, surface):
        super().__init__(x, y, coords, surface)
        self.draw()

    def draw(self):
        # Calculate the points for the X
        top_left = (X_SIZE/2, X_SIZE/2)
        top_right = (self.surface.get_width() - X_SIZE/2, X_SIZE/2 )
        bottom_left = (X_SIZE/2, self.surface.get_height() - X_SIZE/2)
        bottom_right = (self.surface.get_width() - X_SIZE/2 ,self.surface.get_height() - X_SIZE/2)

        # Draw the two lines that make up the X
        pygame.draw.line(self.surface, BLACK, top_left, bottom_right, 5)
        pygame.draw.line(self.surface, BLACK, top_right, bottom_left, 5)

        # print(f"Drew X at {self.coords}")

class O_Obj(Objects):
    def __init__(self, x, y, coords, surface):
        super().__init__(x, y, coords, surface)

    def draw(self):
        border = 4
        center_x = self.surface.get_width() / 2
        center_y = self.surface.get_height() / 2
        radi = X_SIZE

        pygame.draw.circle(self.surface, BLACK, (center_x,center_y), radi, border)

if __name__ == "__main__":
    game = GameLoop()
    game.run()