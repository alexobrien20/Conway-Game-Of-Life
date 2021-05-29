import pygame

class Slider():
    def __init__(self, x, y, width, length, SCREEN, circle_colour, rectangle_colour, min=1, max=100):
        """
        (x,y) = middle of the circle
        width, length = (Width X Length) of the sliding bar
        SCREEN = the surface you want to draw onto
        min,max = the min and the max values you can select
        colour = the colour of each component
        """
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.SCREEN = SCREEN
        self.radius = self.width * 0.75
        self.circle_y_middle = self.y + self.width / 2
        self.circle_x_middle = x
        self.circle_x_max = x + self.length
        self.circle_x_min = x
        self.rectangle_dragging = False
        self.min = min
        self.max = max
        self.circle_colour = circle_colour
        self.rectangle_colour = rectangle_colour

    def draw_slider(self):
        """
        It first draws a clear rectangle over the slider to clear any previous slides
        Checkers the position of the slider to make sure you can't drag it off the screen
        """
        reset_colour = (255, 255, 255)
        reset_y = self.y - (self.radius - self.width * 0.5)
        reset_x = self.x - self.radius
        reset_width = self.width + 2 * (self.radius - self.width * 0.5)
        reset_length = self.length + 2 * self.radius
        rect = pygame.Rect(reset_x, reset_y, reset_length, reset_width)
        pygame.draw.rect(self.SCREEN, reset_colour, rect, 0, 10)

        rect = pygame.Rect(self.x, self.y, self.length, self.width)
        pygame.draw.rect(self.SCREEN, self.rectangle_colour, rect, 0, 10)

        # Checks if the slider is going off the screen
        if self.circle_x_middle >= self.circle_x_max:
            self.circle_x_middle = self.circle_x_max


        if self.circle_x_middle <= self.circle_x_min:
            self.circle_x_middle = self.circle_x_min

        pygame.draw.circle(self.SCREEN, self.circle_colour, (self.circle_x_middle, self.circle_y_middle), self.radius, 0)

    def is_clicked_on(self, event):
        """
        Checked whether the circle has been clicked on 
        Done with pythag
        """
        clicked = False

        mouse_pos= pygame.mouse.get_pos()
        mouse_x_pos = mouse_pos[0]
        mouse_y_pos = mouse_pos[1]

        dx = (mouse_x_pos - self.circle_x_middle) ** 2
        dy = (mouse_y_pos - self.circle_y_middle) ** 2

        if (dx + dy) ** (1/2) <= self.radius and event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        return clicked

    def handle_events(self, event):
        """
        This handles what happens if a user clicks on the circle
        It allows the user to drag the circle and it will redraw the new slider
        -----
        event = iter in pygame.event.get()
        """
        self.draw_slider()
        mouse_position = pygame.mouse.get_pos()
        clicked = self.is_clicked_on(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clicked:
                # If the circle has been clicked then update the picture
                self.rectangle_dragging = True
                self.circle_x_middle = mouse_position[0]
                self.draw_slider()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.rectangle_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            if self.rectangle_dragging:
                # If the circle has been clicked then update the picture
                self.circle_x_middle = mouse_position[0]
                self.draw_slider()

    def slider_level(self):
        """
        Returns the value of the slider at the current position
        """
        percentage_of_length = (self.circle_x_middle - self.x) / self.length 
        value_range = (self.max - self.min)
        value = self.min + value_range * percentage_of_length
        return value