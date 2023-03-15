import pygame


class Input:
    def __init__(self):
        # has the user quit the application?
        self.quit = False

        # lists to store key states
        # down, up: discrete event; lasts for one iteration
        # pressed: continuous event, between down and up events
        self.key_down_list = []
        self.key_pressed_list = []
        self.key_up_list = []

    def update(self):
        # reset discrete key states
        self.key_up_list = []
        self.key_down_list = []

        # iterate over all user input events
        for event in pygame.event.get():
            # Hitting button to close window
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.key_down_list.append(key_name)
                self.key_pressed_list.append(key_name)
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.key_pressed_list.remove(key_name)
                self.key_up_list.append(key_name)

    def is_key_down(self, key_code):
        return key_code in self.key_down_list

    def is_key_up(self, key_code):
        return key_code in self.key_up_list

    def is_key_pressed(self, key_code):
        return key_code in self.key_pressed_list
