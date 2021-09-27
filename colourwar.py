import numpy as np
import pygame
import os
from random import choice
from time import time

COLOURS = [(255, 255, 255), 
           (192, 192, 192), 
           (128, 128, 128), 
           (0, 0, 0), 
           (255, 0, 0), 
           (128, 0, 0), 
           (255, 255, 0), 
           (128, 128, 0), 
           (0, 255, 0), 
           (0, 128, 0), 
           (0, 255, 255), 
           (0, 128, 128), 
           (0, 0, 255), 
           (0, 0, 128), 
           (255, 0, 255), 
           (128, 0, 128)]

# Performance/benchmarking
# ----------------------------------------------------------------
GRID_SIZE = (100, 100) # (WIDTH, HEIGHT)
REPEATS = 10**12
REFRESH = True # improves performance on smaller grids but decreases it on larger ones
DRAW_FREQ = 200 # only applies if REFRESH is True
MAX_FPS = 1000000
# ----------------------------------------------------------------

WIN_SIZE = (1000, 1000)
R_WIDTH = WIN_SIZE[0]/GRID_SIZE[0]
R_HEIGHT = WIN_SIZE[1]/GRID_SIZE[1]

WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("COLOUR WAR")

grid = np.random.randint(len(COLOURS), size=(GRID_SIZE[::-1]))

def neighbours(point, array):
    output = []
    shape = array.shape
    if point[0] > 0:
        output += [(point[0] - 1, point[1])] # TOP
    if point[0] + 1 < shape[0]:
        output += [(point[0] + 1, point[1])] # BOTTOM 
    if point[1] > 0:
        output += [(point[0], point[1] - 1)] # LEFT
    if point[1] + 1 < shape[1]:
        output += [(point[0], point[1] + 1)] # RIGHT
    return output


def unique_neighbours(point, array):
    return [c for c in neighbours(point, array) if grid[c] != grid[point]]


def draw_window(grid):
    WIN.fill((0, 0, 0))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(WIN, COLOURS[grid[i, j]],
                             pygame.Rect(j * R_WIDTH, i * R_HEIGHT, R_WIDTH, R_HEIGHT))    
    pygame.display.update()
        
    
def draw_cell(cell, grid):
    pygame.draw.rect(WIN, COLOURS[grid[cell]], pygame.Rect(cell[1] * R_WIDTH, cell[0] * R_HEIGHT, R_WIDTH, R_HEIGHT))
    pygame.display.update()


def main():
    # Initialize active cells
    active_dict = dict()
    active_list = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if unique_neighbours((i, j), grid):
                active_dict[(i, j)] = True
                active_list += [(i, j)]

    draw_window(grid)
    start = time()

    for i in range(REPEATS):
        pygame.time.Clock().tick(MAX_FPS)
        for event in pygame.event.get():     
            if event.type == pygame.QUIT:
                pygame.quit()

        if active_dict:
            picked_cell = choice(active_list)
            target_cell = choice(unique_neighbours(picked_cell, grid))
            grid[target_cell] = grid[picked_cell]
            
            # Update active cells
            for cell in (neighbours(target_cell, grid) + [target_cell]):
                if not unique_neighbours(cell, grid):
                    if cell in active_dict:
                        del active_dict[cell]
                        active_list.remove(cell)
                elif unique_neighbours(cell, grid):
                    if cell not in active_dict:
                        active_dict[cell] = True
                        active_list += [cell]

            if not REFRESH:
                draw_cell(target_cell, grid)

        if i % DRAW_FREQ == 0 and REFRESH:
            draw_window(grid)
        
    print(time() - start)


if __name__ == "__main__":
    main()
