import pygame
import math
import sys

# Set Vars
SPACE = 10
SCREEN_SIZE = 600
RECT_SIZE = SCREEN_SIZE / 3 - SPACE*2
RECT_AMNT = 3*3

GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class GameLoop:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tic Tac Toe')
        self.win = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))

        # Objects
        self.rects = []
        self.x_obj = []
        self.o_obj = []

        # player control
        # Player 1 is X
        # Player 2 is O
        self.turnWho = 1
        self.turnCounter = 0

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    for i,item in enumerate(self.rects):
                        if item[0].get_rect(topleft=(item[1],item[2])).collidepoint(mouse_pos):
                            grid_coords = self.rect_coords(i)
                            self.player_handle(grid_coords, item)

            self.win.fill(GRAY)

            self.create_input_rects()

            # Update the display
            pygame.display.flip()

    def create_input_rects(self):
        self.rects.clear()
        for i in range(3):
            for j in range(3):
                rect = pygame.Surface((RECT_SIZE,RECT_SIZE))
                y = RECT_SIZE * i*1.1 + SPACE
                x = RECT_SIZE * j*1.1 + SPACE

                rect.fill(WHITE)
                self.win.blit(rect,(x,y))

                self.rects.append([rect,x,y])

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

    def player_handle(self,coords,rect):
        if self.rectAlreadyClicked(coords):
            print(f"{coords} Already selected")
            return

        self.turnCounter += 1
        if self.turnWho == 0: # X
            self.turnWho = 1
            self.x_obj.append(X_Obj(rect[1],rect[2],coords))
        else: # O
            self.turnWho = 0
            self.o_obj.append(O_Obj(rect[1],rect[2],coords))

    def rectAlreadyClicked(self,coords):
        for x in self.x_obj:
            if x.coords == coords:
                return True
        for o in self.o_obj:
            if o.coords == coords:
                return True
        return False

class Objects:
    def __init__(self, x, y, coords):
        self.x = x
        self.y = y
        self.coords = coords # row and col in grid

class X_Obj(Objects):
    def __init__(self, x, y, coords):
        super().__init__(x, y, coords)

    def draw(self):
        return

class O_Obj(Objects):
    def __init__(self, x, y, coords):
        super().__init__(x, y, coords)

if __name__ == "__main__":
    game = GameLoop()
    game.run()