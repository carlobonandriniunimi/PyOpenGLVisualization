from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *


class Test(Base):

    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.vertex_count = None
        self.program_ref = None

    def initialize(self):
        print("Initializing program...")

        vs_code = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """

        fs_code = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 0.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[-1.0, -1.0, 0.0], [1.0, -1.0, 0.0],
                         [1.0, 1.0, 0.0], [-1.0, 1.0, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        self.translation = Uniform("")

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertex_count)

    @staticmethod
    def create_mandelbulb():
        pass


Test().run()
