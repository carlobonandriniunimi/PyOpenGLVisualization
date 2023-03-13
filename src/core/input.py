import pygame


class Input:
    def __init__(self):
        # has the user quit the application?
        self.quit = False

    def update(self):
        # iterate over all user input events
        for event in pygame.event.get():
            # Hitting button to close window
            if event.type == pygame.QUIT:
                self.quit = True
