import pygame
import random
import copy

delay = 100

""" List of all the shapes and thier orientations """

            
class Tetris:
    shapes = {
    'L': ((255, 255, 0), ('010010011', '000111100', '110010010', '001111000')),
    'J': ((255, 165, 0), ('010010110', '100111000', '011010010', '000111001')),
    'S': ((0, 255, 0), ('010011001', '000011110', '100110010', '011110000')),
    'Z': ((128, 0, 128), ('001011010', '000110011', '010110100', '110011000')),
    'T': ((0, 0, 255), ('010011010', '000111010', '010110010', '010111000')),
    'O': ((255,182,193), ('110110000', '110110000', '110110000', '110110000')),
    'I': ((255, 0, 0), ('010010010', '000111000', '010010010', '000111000'))}
    
    def __init__(self):
        self.size = (600, 800)
        self.num_columns = 15
        self.num_rows = 20
        self.grid_pos = [0, 0]
        self.display_grid = [[0 for i in range(self.num_columns)] for i in range(self.num_rows)]
        self.perma_grid = [[0 for i in range(self.num_columns)] for i in range(self.num_rows)]
        self.tick_counter = 0
        self.delay = 100
        self.score = 0
        pygame.init()
        self.display = pygame.display.set_mode((self.size))
        pygame.display.set_caption("Tetris")
        self.new_shape()
        
    def new_shape(self):
        """ Initializes the shape object with a random shape """
        self.color, self.form = random.choice(list(self.shapes.values()))
        self.shape_orientation = random.randint(0, 3)
        self.shape = self.form[self.shape_orientation]
        self.shape_position = [6, 0]
    
    def tick(self):
        self.tick_counter += 1
        if self.tick_counter == self.delay:
            self.tick_counter = 0
            self.shape_position[1] += 1
            if not self.shape_valid():
                self.shape_position[1] -= 1
                self.add_shape(True)
                self.check_tetris()
                self.new_shape()
            self.add_shape()
            self.render_grid()
    
    def check_tetris(self):
        tetris = 0
        self.perma_grid = [row for row in self.perma_grid if not all(row)]
        while len(self.perma_grid) < self.num_rows:
            self.perma_grid.insert(0, [0 for i in range(self.num_columns)])
            tetris += 1
        self.score += [0, 40, 100, 300][tetris]
    
    def shape_valid(self):
        x, y = self.shape_position
        for i, val in enumerate(self.shape):
            if int(val):
                if not (0 <= x + i%3 < self.num_columns and 0 <= y + i//3 < self.num_rows) or self.perma_grid[y + i//3][x + i%3]:
                    return False
        return True
    
    def rotate_shape(self, num):
        """ Rotates the shape num times clockwise """
        self.shape_orientation = (self.shape_orientation + num) % 4
        self.shape = self.form[self.shape_orientation]
        if not self.shape_valid():
            while True:
                x, y = self.shape_position
                for i, val in enumerate(self.shape):
                    if int(val):
                        if x + i%3 < 0:
                            self.shape_position[0] += 1
                            break
                        if x + i%3 >= self.num_columns:
                            self.shape_position[0] -= 1
                            break
                        if y + i//3 < 0:
                            self.shape_position[1] += 1
                            break
                        if y + i//3 >= self.num_rows or self.perma_grid[y + i//3][x + i%3]:
                            self.shape_position[1] -= 1
                            break
                else:
                    break
                continue
    
    def move_shape_right(self):
        self.shape_position[0] += 1
        if not self.shape_valid():
            self.shape_position[0] -= 1
        
    def move_shape_left(self):
        self.shape_position[0] -= 1
        if not self.shape_valid():
            self.shape_position[0] += 1
        
    def drop_shape(self):
        while self.shape_valid():
            self.shape_position[1] += 1
        self.shape_position[1] -= 1
                    
    def add_shape(self, stick=False):
        """ Adds the shape's form to the Tetris grid """
        self.display_grid = copy.deepcopy(self.perma_grid)
        x, y = self.shape_position
        for i, val in enumerate(self.shape):
            if int(val):
                if stick:
                    self.perma_grid[y + i//3][x + i%3] = self.color
                    self.score += 1
                self.display_grid[y + i//3][x + i%3] = self.color
    
    def render_grid(self):
        """ Colors the squares on the Tetris grid according to the status of the grid and the shape """
        self.display.fill((0, 0, 0))
        for y, row in enumerate(self.display_grid):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.display, val, (x*40 + 2, y*40 + 2, 36, 36))
        pygame.display.update()
        

def main():
    game = Tetris()
    clock = pygame.time.Clock()
    run = True
    
    game.add_shape()
    game.render_grid()
    while run:
        clock.tick(100)
        game.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_shape_left()
                    game.add_shape()
                    game.render_grid()
                if event.key == pygame.K_RIGHT:
                    game.move_shape_right()
                    game.add_shape()
                    game.render_grid()
                if event.key == pygame.K_DOWN:
                    game.drop_shape()
                    game.add_shape(stick=True)
                    game.check_tetris()
                    game.new_shape()
                    game.add_shape()
                    game.render_grid()
                if event.key == pygame.K_a:
                    game.rotate_shape(1)
                    game.add_shape()
                    game.render_grid()
                if event.key == pygame.K_d:
                    game.rotate_shape(3)
                    game.add_shape()
                    game.render_grid()
    pygame.quit()

if __name__ == '__main__':
    main()
