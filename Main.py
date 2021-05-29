import pygame
import sys
import numpy as np
from Slider import Slider

class Game():

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT, GRID_WIDTH, BLOCK_SIZE):
        """
        Make sure that SCREEN_WIDTH / BLOCKSIZE == an integer?
        """
        pygame.init()
        pygame.font.init()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.GRID_HEIGHT = GRID_HEIGHT
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HISTORY = [np.zeros([int(self.GRID_WIDTH / self.BLOCK_SIZE), int(self.GRID_HEIGHT / self.BLOCK_SIZE)])]
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.SCREEN.fill((255,255,255))
        self.iteration = 0
        self.GAME_FONT = int(min(self.SCREEN_HEIGHT*0.05, self.SCREEN_WIDTH*0.05))
        self.MY_FONT = pygame.font.SysFont('georgia', self.GAME_FONT)

    def start_game(self):
        """
        The first loop that starts the game
        On the first screen you choose squares that are alive or dead
        Then you start the simulation after that
        """
        clock = pygame.time.Clock()
        clock.tick(25)

        running = True
        game_started = False
        next_pressed = False

        # Init grid setup
        # Draws the Blank grid, slider, 4 Buttons, Speed Icon

        self.draw_grid()
        button_objects = self.draw_buttons()
        slider = Slider(self.SCREEN_WIDTH*0.25,self.SCREEN_HEIGHT*0.95, self.SCREEN_HEIGHT*0.02, self.SCREEN_WIDTH*0.5, self.SCREEN, (0,0,0), (255,0,0))
        slider.draw_slider()
        slider_clicked = False
        speed_icon  = pygame.image.load('speed_icon.png')
        speed_icon = pygame.transform.scale(speed_icon, (int(self.SCREEN_HEIGHT*0.07), int(self.SCREEN_WIDTH*0.07)))
        self.SCREEN.blit(speed_icon, (self.SCREEN_WIDTH*0.77, self.SCREEN_HEIGHT*0.92))

        # Sets up an event to call the game logic every 2000 milliseconds
        one_iteration_event = pygame.USEREVENT + 1
        one_iteration_speed = 2000
        pygame.time.set_timer(one_iteration_event, one_iteration_speed)

        while running:
            # Main Game Loop
            for event in pygame.event.get():
                # Slider logic
                slider.handle_events(event)
                if slider.is_clicked_on(event):
                    slider_clicked = True
                if event.type == pygame.MOUSEBUTTONUP and slider_clicked == True:
                    slider_clicked = False
                    one_iteration_speed = 2000 - 18 * int(slider.slider_level())
                    pygame.time.set_timer(one_iteration_event, one_iteration_speed)
                # Exit logic
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)
                # Checkers whether to perfrom one iteration
                elif event.type == one_iteration_event and game_started == True:
                    # Checks if the game has started
                    # And checks if the game event should be happening
                    # If both true then perfroms one interation
                    self.one_game_iter()
                    self.draw_grid_array()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_objects[0].collidepoint((mouse_x, mouse_y)):
                        # Checks if the start button is pressed
                        # If pressed then the game is started
                        # If game has started then the game stops when pressed again
                        game_started = not game_started
                        game_button_text = ['Start', 'Stop'][game_started]
                        self.redraw_buttons(game_button_text, 'START')
                        self.redraw_buttons('Reset', 'RESET')
                        reset_button = True
                    elif button_objects[1].collidepoint((mouse_x, mouse_y)) and game_started == False:
                        # Checks if next was pressed and game is not running
                        # Then perform one iteration
                        next_pressed = True
                        reset_button = True
                        self.redraw_buttons('Reset', 'RESET')
                        self.one_game_iter()
                        self.draw_grid_array()
                    elif button_objects[2].collidepoint((mouse_x, mouse_y)) and game_started == False:
                        # Checks if back was pressed
                        # Takes the game back one iteration
                        # Checks if your back at the start
                        if self.iteration == 0: 
                            pass
                        else:
                            del self.GRID_HISTORY[self.iteration]
                            self.iteration -= 1
                            self.draw_grid_array()
                    elif button_objects[3].collidepoint((mouse_x, mouse_y)):
                        # Checks if this button was pressed
                        # Starts as clear
                        # If start is pressed then it does to reset
                        if next_pressed:
                            # If the game has started then the button should first say reset
                            # Resets the game back to iteration 0
                            self.iteration = 0
                            self.draw_grid_array()
                            game_started = False
                            self.redraw_buttons('Start','START')
                            self.redraw_buttons('Clear','RESET')
                            next_pressed = False
                            reset_button = False
                        elif reset_button:
                            self.iteration = 0
                            self.redraw_buttons('Clear','RESET')
                            self.redraw_buttons('Start','START')
                            game_started = False
                            self.draw_grid_array()
                            reset_button = False
                        else:
                            self.GRID_HISTORY = [np.zeros([int(self.GRID_WIDTH / self.BLOCK_SIZE), int(self.GRID_HEIGHT / self.BLOCK_SIZE)])]
                            self.iteration = 0
                            self.draw_grid_array()
                    elif game_started == False:
                        if mouse_y > self.GRID_HEIGHT:
                            # If your mouse is clicking lower than the grid then don't add squares
                            pass
                        else:
                            if event.button == 1:
                                # Left mouse click
                                # Get the mouse positon and turn that square black 
                                # (i.e that square is now alive)
                                alive = 1
                                colour = (0,0,0)
                                self.colour_square(colour, alive)
                            elif event.button == 3:
                                # Right mouse click
                                # Turn that square white
                                # (i.e that sqaure is now dead)
                                alive = 0
                                colour = (255,255,255)
                                self.colour_square(colour, alive)
            pygame.display.update()

    def redraw_buttons(self, text, type):
        """
        Redraws the start and reset buttons
        text = text value of the button
        type = whether to redraw the start or reset button
        """
        rect_y_pos = self.GRID_HEIGHT + (self.SCREEN_HEIGHT - self.GRID_HEIGHT) * 0.10 
        rect_length = self.GRID_WIDTH * 0.2
        rect_height = (self.SCREEN_HEIGHT - self.GRID_HEIGHT) * 0.40
        rect_colour = (196, 139, 240)
        coordinates = {'START' : ((self.GRID_WIDTH) - rect_length * 4 ) / 5, 
                        'RESET' : ((self.GRID_WIDTH) - rect_length * 4 ) / 5 * (4) + rect_length * 3}
        rect_x_pos = int(coordinates[type])
        rect = pygame.Rect(rect_x_pos, rect_y_pos, rect_length, rect_height)
        pygame.draw.rect(self.SCREEN, rect_colour, rect, 0, 25)
        text_surface = self.MY_FONT.render(text, True, (0,0,0))
        text_y_pos = rect.y + rect.height / 8
        text_x_pos = rect.x + rect.width / 4 
        self.SCREEN.blit(text_surface,(text_x_pos, text_y_pos))

    def draw_buttons(self):
        """
        Fits 4 buttons on to the screen.
        Returns references to the buttons + text
        """
        button_text = ['Start', 'Next', 'Back', 'Clear']
        button_objects = []
        rect_y_pos = self.GRID_HEIGHT + (self.SCREEN_HEIGHT - self.GRID_HEIGHT) * 0.10
        rect_length = self.GRID_WIDTH * 0.2
        rect_height = (self.SCREEN_HEIGHT - self.GRID_HEIGHT) * 0.40
        rect_colour = (196, 139, 240)

        button_gap = ((self.GRID_WIDTH) - rect_length * 4 ) / 5

        #Draw the 4 buttons seperated by button_gap
        for i in range(4):
            rect_x_pos = button_gap * (i+1) + rect_length * i
            rect = pygame.Rect(rect_x_pos, rect_y_pos, rect_length, rect_height)
            pygame.draw.rect(self.SCREEN, rect_colour, rect, 0, 25)
            text = button_text[i]
            text_surface = self.MY_FONT.render(text, True, (0,0,0))
            text_y_pos = rect.y + rect.height / 8
            text_x_pos = rect.x + rect.width / 4 
            self.SCREEN.blit(text_surface,(text_x_pos, text_y_pos))
            button_objects.append(rect)

        return button_objects

    def colour_square(self, colour, alive):
        """
        colour = (255,255,255) or (0,0,0)
        Turns the selected square white or black
        Right click = white
        Left click = black
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_x // self.BLOCK_SIZE, mouse_y // self.BLOCK_SIZE
        self.GRID_HISTORY[self.iteration][mouse_x, mouse_y] = alive
        x_pos = mouse_x * self.BLOCK_SIZE + 1
        y_pos = mouse_y * self.BLOCK_SIZE + 1
        rect = pygame.Rect(x_pos,y_pos, self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
        pygame.draw.rect(self.SCREEN, colour, rect, 0)

    def draw_grid(self):
        """
        Sets up the intial grid with every square 'dead'
        """
        for x in range(0, self.GRID_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.GRID_HEIGHT, self.BLOCK_SIZE):
                rect = pygame.Rect(x,y, self.BLOCK_SIZE, self.BLOCK_SIZE)
                pygame.draw.rect(self.SCREEN, (211,211,211), rect, 1)

    def check(self, x, y, alive):
        """
        Carries our the logic of the Game of Life
        Counts how many neighbours each cell has. 
        """
        states = [0,-1]
        neighbours = states[alive]
        
        x_upper_limit = 2
        x_lower_limit = -1
        
        y_upper_limit = 2
        y_lower_limit = -1
        
        if x == self.GRID_HISTORY[0].shape[0] - 1:
            x_upper_limit = 1
        if x == 0: 
            x_lower_limit = 0
        if y == self.GRID_HISTORY[0].shape[1] - 1:
            y_upper_limit = 1
        if y == 0: 
            y_lower_limit = 0
            
        for i in range(x_lower_limit,x_upper_limit):
            for j in range(y_lower_limit, y_upper_limit):
                if self.GRID_HISTORY[self.iteration][x+i, y+j] == 1:
                    neighbours += 1
        return neighbours

    def one_game_iter(self):
        """
        Performs one interation of Conways Game of Life.
        """
        NEW_ARRAY = np.zeros([self.GRID_HISTORY[0].shape[0], self.GRID_HISTORY[0].shape[1]])
        current_grid = self.GRID_HISTORY[self.iteration]
        for i in range(current_grid.shape[0]):
            for j in range(current_grid.shape[1]):
                current_cell = int(current_grid[i,j])
                cell_neighbours = self.check(i, j, current_cell)
                if current_cell == 1:
                    # If 1 then the cell is currently alive
                    if cell_neighbours < 2 or cell_neighbours > 3:
                        NEW_ARRAY[i, j] = 0
                    else:
                        NEW_ARRAY[i,j] = 1
                else:
                    # Else the cell is 0 hence dead
                    # If it has 3 neighbours bring that cell to life
                    if cell_neighbours == 3:
                        NEW_ARRAY[i, j] = 1
        self.GRID_HISTORY.append(NEW_ARRAY)
        self.iteration += 1

    def draw_grid_array(self):
        """
        Draws the grid on the screen
        white = dead
        black = alive
        """
        for i in range(self.GRID_HISTORY[0].shape[0]):
            for j in range(self.GRID_HISTORY[0].shape[1]):
                cell_alive = self.GRID_HISTORY[self.iteration][i,j]
                if cell_alive == 1:
                    colour = (0,0,0)
                else:
                    colour = (255,255,255)
                x_pos = i * self.BLOCK_SIZE + 1
                y_pos = j * self.BLOCK_SIZE + 1
                rect = pygame.Rect(x_pos,y_pos, self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
                pygame.draw.rect(self.SCREEN, colour, rect, 0)

if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRID_WIDTH = 800
    GRID_HEIGHT = 500
    BLOCK_SIZE = 20
    GameOfLife = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT, GRID_WIDTH, BLOCK_SIZE)
    GameOfLife.start_game()
