import pygame
import sys
import numpy as np


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

clock = pygame.time.Clock()

def main():
    GRID_ARRAY = np.zeros([40,30])
    pygame.init()
    clock.tick(25)

    running = True

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill((255,255,255))
    draw_grid(SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN, BLOCK_SIZE)

    while running:
        #rect = pygame.Rect(1,1, 19,19)
        #pygame.draw.rect(SCREEN, (0,0,0), rect, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #START THE GAME
                    #run_game(GRID_ARRAY)
                    GRID_ARRAY = one_game_iter(GRID_ARRAY)
                    draw_grid_array(GRID_ARRAY, SCREEN)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left mouse click
                    # Get the mouse positon and turn that square black
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x, mouse_y = mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE
                    GRID_ARRAY[mouse_x, mouse_y] = 1
                    x_pos = mouse_x * BLOCK_SIZE + 1
                    y_pos = mouse_y * BLOCK_SIZE + 1
                    rect = pygame.Rect(x_pos,y_pos, BLOCK_SIZE - 2,BLOCK_SIZE - 2)
                    pygame.draw.rect(SCREEN, (0,0,0), rect, 0)
                elif event.button == 3:
                    #right mouse click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x, mouse_y = mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE
                    GRID_ARRAY[mouse_x, mouse_y] = 0
                    x_pos = mouse_x * BLOCK_SIZE + 1
                    y_pos = mouse_y * BLOCK_SIZE + 1
                    rect = pygame.Rect(x_pos,y_pos, BLOCK_SIZE - 2,BLOCK_SIZE - 2)
                    pygame.draw.rect(SCREEN, (255,255,255), rect, 0)


        
        pygame.display.update()


def run_game(GRID_ARRAY):
    pygame.init()
    clock.tick(25)

    running = True

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill((255,255,255))
    draw_grid(SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN, BLOCK_SIZE)

    while running:
        GRID_ARRAY = one_game_iter(GRID_ARRAY)
        draw_grid_array(GRID_ARRAY, SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)
        
        pygame.display.update()

def draw_grid_array(GRID_ARRAY, SCREEN):
    for i in range(GRID_ARRAY.shape[0]):
        for j in range(GRID_ARRAY.shape[1]):
            cell_alive = GRID_ARRAY[i,j]
            if cell_alive == 1:
                colour = (0,0,0)
            else:
                colour = (255,255,255)
            x_pos = i * BLOCK_SIZE + 1
            y_pos = j * BLOCK_SIZE + 1
            rect = pygame.Rect(x_pos,y_pos, BLOCK_SIZE - 2,BLOCK_SIZE - 2)
            pygame.draw.rect(SCREEN, colour, rect, 0)

def check(GRID_ARRAY, x, y, alive):
    states = [0,-1]
    neighbours = states[alive]
    
    x_upper_limit = 2
    x_lower_limit = -1
    
    y_upper_limit = 2
    y_lower_limit = -1
    
    if x == GRID_ARRAY.shape[0] - 1:
        x_upper_limit = 1
    if x == 0: 
        x_lower_limit = 0
    if y == GRID_ARRAY.shape[1] - 1:
        y_upper_limit = 1
    if y == 0: 
        y_lower_limit = 0
        
    for i in range(x_lower_limit,x_upper_limit):
        for j in range(y_lower_limit, y_upper_limit):
            if GRID_ARRAY[x+i, y+j] == 1:
                neighbours += 1
    return neighbours
        
def one_game_iter(GRID_ARRAY):
    NEW_ARRAY = np.zeros([GRID_ARRAY.shape[0], GRID_ARRAY.shape[1]])
    for i in range(GRID_ARRAY.shape[0]):
        for j in range(GRID_ARRAY.shape[1]):
            current_cell = int(GRID_ARRAY[i,j])
            cell_neighbours = check(GRID_ARRAY, i, j, current_cell)
            if current_cell == 1:
                print(f"{i,j,cell_neighbours}")
                # If 1 then the cell is currently alive
                if cell_neighbours < 2 or cell_neighbours > 3:
                    NEW_ARRAY[i, j] = 0
                else:
                    NEW_ARRAY[i,j] = 1
            else:
                # Else the cell is 0 hence dead
                # If it has 3 neighbours bring that cell to life
                if cell_neighbours == 3:
                    print("CREATING LIFE!")
                    NEW_ARRAY[i, j] = 1
    return NEW_ARRAY

def draw_grid(SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN, BLOCK_SIZE):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x,y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (211,211,211), rect, 1)




if __name__ == '__main__':
    main()

    
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

clock = pygame.time.Clock()

def main():
    pygame.init()
    clock.tick(25)

    running = True
    rectangle_dragging = False

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill((255,255,255))
    circle_colour = (0,0,0)
    slider_colour = (255,0,0)
    my_slider = Slider(100, 100, 50, 200, SCREEN, circle_colour, slider_colour, min=0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)

            my_slider.handle_events(event)
            print(f"VOLUME : {my_slider.slider_level()}")

        pygame.display.update()