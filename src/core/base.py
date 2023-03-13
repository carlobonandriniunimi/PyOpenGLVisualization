import sys

import pygame

from .input import Input
from .openGLUtils import OpenGLUtils


class Base:
    def __init__(self, screen_size=None):
        if screen_size is None:
            screen_size = [512, 512]
        # initialize all pygame modules
        pygame.init()
        # indicate rendering details
        # DOUBLEBUFF means one buffer is the one being rendered,
        # the other is the one we are calculating (display.flip)
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        # initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # use a core OpenGL profile for cross-platform compatibility
        # CORE profiles only guaranties the current version of API
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE)
        # create and display the window
        self.screen = pygame.display.set_mode(screen_size, display_flags)
        # set title bar
        pygame.display.set_caption("Graphics window")

        # determine if main loop is active
        self.running = True
        # manage time-related data and operations
        self.clock = pygame.time.Clock()

        # manage user input
        self.input = Input()

    # implement by extending class
    def initialize(self):
        pass

    # implement by extending class
    def update(self):
        pass

    def run(self):
        # startup
        self.initialize()

        OpenGLUtils.print_system_info()

        # main loop
        while self.running:
            # process input
            self.input.update()
            if self.input.quit:
                self.running = False

            # update
            self.update()

            # render
            # display image on screen
            pygame.display.flip()

            # pause if necessary to achieve 60 FPS
            self.clock.tick(60)

        # shutdown
        pygame.quit()
        sys.exit()
