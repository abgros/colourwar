import numpy as np
import pygame
import cv2
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

# Settings
# ----------------------------------------------------------------
WIN_SIZE = (1000, 1000) # (HEIGHT, WIDTH)
GRID_SIZE = (100, 100) # (HEIGHT, WIDTH)
REPEATS = 10**12
MAX_FPS = 1000000

# This setting, if enabled causes the entire grid to refresh every DRAW_FREQ iterations.
# If disabled, the program only draws a single cell every iteration.
# Enabling it improves performance on smaller grids but decreases it on larger ones.
REFRESH = True

# If REFRESH is True, this controls how often the displayed grid refreshes.
DRAW_FREQ = 200

# You can read an image to start
# It might take some time if it's a large image
# The size of the image will override GRID_SIZE
image_path = None

# ----------------------------------------------------------------


def set_grid(GRID_SIZE, image_path):
    if image_path:
        grid = []
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR -> RGB
        for row in range(len(img)):
            grid += [[]]
            for col in range(len(img[row])):
                p = tuple(img[row, col])
                if p in COLOURS:
                    p = COLOURS.index(p)
                else:
                    p = 0
                grid[row] += [p]
            if row % 50 == 49 and row > 0:
                print("Read row", row + 1)
        grid = np.array(grid)
    else:
        grid = np.random.randint(len(COLOURS), size=(GRID_SIZE))

    return grid


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
    return [c for c in neighbours(point, array) if array[c] != array[point]]


def draw_window(WIN, grid):
    cell_height = WIN_SIZE[0]/grid.shape[0]
    cell_width = WIN_SIZE[1]/grid.shape[1]
    
    WIN.fill((0, 0, 0))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(WIN, COLOURS[grid[i, j]],
                             pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height))    
    pygame.display.update()
        
    
def draw_cell(WIN, cell, grid):
    cell_height = WIN_SIZE[0]/grid.shape[0]
    cell_width = WIN_SIZE[1]/grid.shape[1]
    
    pygame.draw.rect(WIN, COLOURS[grid[cell]], pygame.Rect(cell[1] * cell_width, cell[0] * cell_height, cell_width, cell_height))
    pygame.display.update()


def main():
    # Initialize window
    WIN = pygame.display.set_mode(WIN_SIZE[::-1]) # WIN_SIZE is (width, height) so I invert it for consistency
    pygame.display.set_caption("COLOUR WAR")
    grid = set_grid(GRID_SIZE, image_path)
    draw_window(WIN, grid)
    
    # Initialize active cells
    active_dict = dict()
    active_list = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if unique_neighbours((i, j), grid):
                active_dict[(i, j)] = True
                active_list += [(i, j)]

    start = time()

    # Game loop
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
                draw_cell(WIN, target_cell, grid)

        if i % DRAW_FREQ == 0 and REFRESH:
            draw_window(WIN, grid)
        
    print(time() - start)


if __name__ == "__main__":
    main()
