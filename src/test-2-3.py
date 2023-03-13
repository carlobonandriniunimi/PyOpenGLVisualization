from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *


class Test(Base):
    """Render six points in a hexagon arrangement"""

    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.vertex_count = None
        self.program_ref = None

    def initialize(self):
        print("Initializing program...")

        # initialize program
        vs_code = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x, position.y, 
                position.z, 1.0);
        }
        """
        fs_code = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        # render settings (optional)
        glLineWidth(1)

        # set up vertex array object
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # set up vertex attribute
        position_data = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0],
                         [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0],
                         [-0.4, -0.6, 0.0], [0.4, -0.6, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

    def update(self):
        glUseProgram(self.program_ref)
        # try GL_LINES, GL_LINE_STRIP, GL_TRIANGLES,
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)


# instantiate this class and run the program
Test().run()
