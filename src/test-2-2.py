from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *


# render a single point
class Test(Base):

    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.program_ref = None

    def initialize(self):
        print("Initializing program...")

        # initialize program

        # vertex shader code
        # draw at the center of the screen
        vs_code = """
        void main()
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
        }
        """

        # fragment shader code
        fs_code = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        # send code to GPU adn compile, store program ref
        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)
        # set up vertex array object
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # render settings (optional)

        # set point width and height
        glPointSize(10)

    def update(self):
        # select program to use when rendering
        glUseProgram(self.program_ref)

        # renders geometric objects using selected program
        glDrawArrays(GL_POINTS, 0, 1)


# instantiate this class and run the program
Test().run()
