import time

import numpy as np
from numba import jit

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
        in vec2 position;
        in vec4 color;
        out vec4 out_color;
        void main()
        {
            gl_Position = vec4(position.x, position.y, 
                0.0, 1.0);
            out_color = color;
        }
        """
        fs_code = """
        in vec4 out_color;
        out vec4 fragColor;
        void main()
        {
            fragColor = out_color;
        }
        """

        self.program_ref = OpenGLUtils.initialize_program(vs_code, fs_code)

        # set up vertex array object
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # set up vertex attribute
        start = time.time()
        position_data, color_data = gen_mandelbrot(self.screen.get_width(), self.screen.get_height())
        print(f"Time took: {time.time() - start}")
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec2", position_data)
        position_attribute.associate_variable(self.program_ref, "position")
        color_attribute = Attribute("vec4", color_data)
        color_attribute.associate_variable(self.program_ref, "color")

    def update(self):
        glUseProgram(self.program_ref)
        glDrawArrays(GL_POINTS, 0, self.vertex_count)


@jit
def gen_mandelbrot(width, height):
    r1 = np.linspace(-2.0, 0.5, width)
    r2 = np.linspace(-1.25, 1.25, height)
    points = []
    colors = []
    max_iter = 2048
    for i in range(width):
        for j in range(height):
            iter_count = mandelbrot(r1[i] + 1j * r2[j], max_iter)
            x = np.interp(i, [0, width], [-1, 1])
            y = np.interp(j, [0, height], [-1, 1])
            points.append([x, y])
            color_x = iter_count / max_iter
            if color_x > 0.5:
                colors.append([color_x, 1.0, color_x, 1.0])
            else:
                colors.append([0.0, color_x, 0.0, 1.0])

    return points, colors


@jit
def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return n
        z = z * z + c
    return 0


# instantiate this class and run the program
Test([1024, 1024]).run()
