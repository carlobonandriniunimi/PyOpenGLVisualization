from math import pi, atan2, sin, cos, sqrt

from OpenGL.GL import *
import numpy as np
from numba import jit
import time

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from core.input import Input


class Test(Base):
    def __init__(self, screen_size=None):
        super().__init__(screen_size)

    def initialize(self):
        vs_code = """
        in vec3 position;
        out vec4 fragPos;
        uniform mat4 projectionMatrix;
        uniform mat4 model_matrix;
        void main() {
            gl_Position = projectionMatrix * model_matrix *
                vec4(position, 1.0);
            fragPos = vec4(position, 1.0);
        }
        """

        fs_code = """
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 1.0, 1.0, 0.0);
        }
        """

        fs_code_mandelbulb = """
        in vec4 fragPos;
        out vec4 fragColor;
        void main() {
            int n = 8;
            float x = fragPos.x;
            float y = fragPos.y;
            float z = fragPos.z;
            vec3 v = vec3(x, y, z);
            vec3 arr = vec3(x, y, z);
            bool flag = false;
            float max = pow(2, n);
            for(int i = 0; i < 100; i++) {
                float r = sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
                float o = atan(v.y, v.x);
                float O = atan(sqrt(v.x * v.x + v.y * v.y), z);
                float r_n = pow(r, n);
                vec3 v_n = vec3(sin(n*O)*cos(n*o) * r_n, sin(n*O)*sin(n*o) * r_n, cos(n*O) * r_n);

                v = v_n + arr;

                if (r > max) {
                    fragColor = vec4(0.0, 0.0, 0.0, 1.0);
                    flag = true;
                    break;
                }
            }
            if(flag == false) {
                fragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
        }
        """
        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        ## Render settings ##
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # start = time.time()
        position_data = createBulb(n=8, space_len=100).tolist()
        # position_data = createSpace(space_len=100).tolist()
        # print(time.time() - start)

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

        self.move_speed = 2.0
        # rotation speed, radians per second
        self.turn_speed = 90 * (pi / 180)

    def update(self):
        # update data
        turn_amount = self.turn_speed * self.delta_time
        move_amount = self.move_speed * self.delta_time

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
        glDrawArrays(GL_POINTS, 0, self.vertex_count)


@jit(nopython=True)
def createSpace(space_len):
    max_len = space_len**3
    position_data = np.empty((max_len, 3))
    count = 0
    for x in np.linspace(-1, 1, space_len):
        for y in np.linspace(-1, 1, space_len):
            for z in np.linspace(-1, 1, space_len):
                position_data[count] = [x, y, z]
                count += 1
    return position_data


@jit(nopython=True)
def createBulb(n, space_len, max_iter=100):
    max_len = space_len**3
    position_data = np.empty((max_len, 3))
    count = 0
    for x in np.linspace(-1, 1, space_len):
        for y in np.linspace(-1, 1, space_len):
            edge = False
            for z in np.linspace(-1, 1, space_len):
                arr = np.array([x, y, z])
                v = np.array([x, y, z])
                flag = False
                for _ in range(max_iter):
                    r = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
                    o = atan2(v[1], v[0])
                    O = atan2(sqrt(v[0]*v[0] + v[1]*v[1]), v[2])
                    r_n = r**n
                    v_n = np.array([(sin(n*O)*cos(n*o) * r_n),
                                    (sin(n*O)*sin(n*o) * r_n),
                                    (cos(n*O) * r_n)])

                    v = v_n + arr

                    if r > (2**n):
                        if edge:
                            edge = False
                        flag = True
                        break
                if not flag and not edge:
                    edge = True
                    position_data[count] = arr
                    count += 1

    return position_data[:count]


Test(screen_size=[1024, 1024]).run()
