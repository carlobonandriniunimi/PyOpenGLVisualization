from core.base import Base
from openGLUtils import OpenGLUtils
from attribute import Attribute
from uniform import Uniform
from OpenGL.GL import *


class Test(Base):
    """Draw a keyboard controlled triangle"""

    def __init__(self, screen_size=None):
        super().__init__(screen_size)
        self.base_color = None
        self.translation = None
        self.vertex_count = None
        self.program_ref = None
        self.speed = None

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
            fragColor = vec4(
            baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        # !!!!!! render settings
        # set color for glClear
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # set up vertex array object
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # set up vertex attribute
        position_data = [[0.0, 0.2, 0.0], [0.2, -0.2, 0.0], [-0.2, -0.2, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        # set up uniforms
        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, "translation")
        self.base_color = Uniform("vec3", [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, "baseColor")

        # triangle speed, units per second
        self.speed = 2.0

    def update(self):
        distance = self.speed * self.delta_time
        # Not elif to allow multiple key presses at the same time
        if self.input.is_key_pressed("left"):
            self.translation.data[0] -= distance
        if self.input.is_key_pressed("right"):
            self.translation.data[0] += distance
        if self.input.is_key_pressed("down"):
            self.translation.data[1] -= distance
        if self.input.is_key_pressed("up"):
            self.translation.data[1] += distance

        # reset color buffer
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


Test().run()
