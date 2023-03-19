from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from core.input import Input
from OpenGL.GL import *
from math import pi


class Test(Base):
    def initialize(self):
        vs_code = """
        in vec3 position;
        uniform mat4 projectionMatrix;
        uniform mat4 model_matrix;
        void main() {
            gl_Position = projectionMatrix * model_matrix *
                vec4(position, 1.0);
        }
        """

        fs_code = """
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """
        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        ## Render settings ##
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [[0.0, 0.2, 0.0], [0.1, -0.2, 0.0],
                         [-0.1, -0.2, 0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        ## Set up uniforms ##
        m_matrix = Matrix.makeTranslation(0, 0, -1)
        self.model_matrix = Uniform("mat4", m_matrix)
        self.model_matrix.locate_variable(self.program_ref, "model_matrix")

        p_matrix = Matrix.makePerspective()
        self.projection_matrix = Uniform("mat4", p_matrix)
        self.projection_matrix.locate_variable(self.program_ref,
                                               "projectionMatrix")

        # movement speed, units per second
        self.move_speed = 0.5
        # rotation speed, radians per second
        self.turn_speed = 90 * (pi / 180)

    def update(self):
        # update data
        move_amount = self.move_speed * self.delta_time
        turn_amount = self.turn_speed * self.delta_time

        # global translation (fixed axis)
        if self.input.is_key_pressed("w"):
            m = Matrix.makeTranslation(0, move_amount, 0)
            # matrix multiplication between old transform and new
            # translation (@ for matrix-mult)
            self.model_matrix.data = m @ self.model_matrix.data
        elif self.input.is_key_pressed("s"):
            m = Matrix.makeTranslation(0, -move_amount, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed("a"):
            m = Matrix.makeTranslation(-move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed("d"):
            m = Matrix.makeTranslation(move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed("z"):
            m = Matrix.makeTranslation(0, 0, move_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed("x"):
            m = Matrix.makeTranslation(0, 0, -move_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        # global rotation (around the origin) (rotation z-axis)
        if self.input.is_key_pressed("q"):
            m = Matrix.makeRotationZ(turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed("e"):
            m = Matrix.makeRotationZ(-turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data

        # local translation
        if self.input.is_key_pressed("i"):
            m = Matrix.makeTranslation(0, move_amount, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed("k"):
            m = Matrix.makeTranslation(0, -move_amount, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed("j"):
            m = Matrix.makeTranslation(-move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed("l"):
            m = Matrix.makeTranslation(move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m

        # local rotation (around object center z-axis)
        if self.input.is_key_pressed("u"):
            m = Matrix.makeRotationZ(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed("o"):
            m = Matrix.makeRotationZ(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m

        # local rotation (y-axis)
        if self.input.is_key_pressed("c"):
            m = Matrix.makeRotationY(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed("v"):
            m = Matrix.makeRotationY(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m

        ## render scene ##
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_ref)
        self.projection_matrix.upload_data()
        self.model_matrix.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


Test().run()
