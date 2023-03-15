from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *


class Test(Base):
    """Render two triangles with different positions and colors"""

    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.base_color1 = None
        self.base_color2 = None
        self.translation2 = None
        self.translation1 = None
        self.vertex_count = None
        self.program_ref = None

    def initialize(self):
        print("Initializing program...")

        vs_code = """
        in vec3 position;
        uniform vec3 translation;
        void main()
        {
            vec3 pos = position + translation;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """

        fs_code = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[0.0, 0.2, 0.0], [0.2, -0.2, 0.0],
                         [-0.2, -0.2, 0.0]]
        self.vertex_count = len(position_data)
        position_attr = Attribute("vec3", position_data)
        position_attr.associate_variable(self.program_ref, "position")

        # settings up uniforms
        self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation1.locate_variable(self.program_ref, "translation")
        self.translation2 = Uniform("vec3", [0.5, 0.0, 0.0])
        self.translation2.locate_variable(self.program_ref, "translation")

        self.base_color1 = Uniform("vec3", [1.0, 0.0, 0.0])
        self.base_color1.locate_variable(self.program_ref, "baseColor")
        self.base_color2 = Uniform("vec3", [0.0, 0.0, 1.0])
        self.base_color2.locate_variable(self.program_ref, "baseColor")

    def update(self):
        glUseProgram(self.program_ref)

        # draw the first triangle
        self.translation1.upload_data()
        self.base_color1.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        # draw the second triangle
        self.translation2.upload_data()
        self.base_color2.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


Test().run()
