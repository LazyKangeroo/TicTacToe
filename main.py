import pygame
import math
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

        self.create_rect()

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
            for x in self.x_obj:
                x.draw()
            self.display_rects()
            # for o in self.o_obj:
                # o.draw()

            # Update the display
            pygame.display.flip()

    def create_rect(self):
        for i in range(3):
            for j in range(3):
                rect = pygame.Surface((RECT_SIZE,RECT_SIZE))
                y = RECT_SIZE * i*1.1 + SPACE
                x = RECT_SIZE * j*1.1 + SPACE
                rect.fill(WHITE)

                self.rects.append([rect,x,y])

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

    def player_handle(self,coords,rect):
        if self.rectAlreadyClicked(coords):
            print(f"{coords} Already selected")
            return
        if self.turnWho == 0: # X
            self.turnWho = 1
            self.x_obj.append(X_Obj(rect[1],rect[2],coords, rect[0]))
        else: # O
            self.turnWho = 0
            self.o_obj.append(O_Obj(rect[1],rect[2],coords, rect[0]))

    def rectAlreadyClicked(self,coords):
        for x in self.x_obj:
            if x.coords == coords:
                return True
        for o in self.o_obj:
            if o.coords == coords:
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
        bottom_left = (X_SIZE/2, self.surface.get_height() - X_SIZE/2   )
        bottom_right = (self.surface.get_width() - X_SIZE/2 ,self.surface.get_height() - X_SIZE/2   )

        # draw_surface = self.surface.subsurface((0,0))
        # Draw the two lines that make up the X
        pygame.draw.line(self.surface, BLACK, top_left, bottom_right, 5)
        pygame.draw.line(self.surface, BLACK, top_right, bottom_left, 5)

        print(f"Drew X at {self.coords}")

class O_Obj(Objects):
    def __init__(self, x, y, coords, surface):
        super().__init__(x, y, coords, surface)

if __name__ == "__main__":
    game = GameLoop()
    game.run()