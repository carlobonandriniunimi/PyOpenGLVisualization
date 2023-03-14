from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *


class Test(Base):
    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.program_ref = None
        self.vertex_count = None

    def initialize(self):
        print("Initializing program...")

        vs_code = """
        in vec3 vertex_color;
        in vec3 position;
        out vec4 color;
        void main() 
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            color = vec4(vertex_color.r, vertex_color.g, vertex_color.b, 1.0);
        }
        """

        fs_code = """
        in vec4 color;
        out vec4 fragColor;
        void main() 
        {
            fragColor = color;
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        # glPointSize(10)
        # glLineWidth(4)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0],
                         [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0],
                         [-0.4, -0.6, 0.0], [0.4, -0.6, 0.0]]
        self.vertex_count = len(position_data)
        position_attr = Attribute("vec3", position_data)
        position_attr.associate_variable(self.program_ref, "position")

        color_data = [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0],
                      [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                      [0.0, 0.0, 1.0], [0.5, 0.0, 1.0]]
        color_attr = Attribute("vec3", color_data)
        color_attr.associate_variable(self.program_ref, "vertex_color")

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertex_count)


Test().run()
