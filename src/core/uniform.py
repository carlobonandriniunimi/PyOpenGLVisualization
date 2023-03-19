from OpenGL.GL import *


class Uniform:
    def __init__(self, data_type, data):
        # type of data:
        # int | bool | float | vec2 | vec3 | vec4 | mat4
        self.data_type = data_type
        # data to be sent to uniform variable
        self.data = data

        # reference for variable location in program
        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name):
        """Get and store reference for program variable with given name"""
        self.variable_ref = glGetUniformLocation(program_ref, variable_name)

    def upload_data(self):
        """Store data in uniform variable previously located"""
        # if the program does not reference the variable, exit
        if self.variable_ref == -1:
            return

        if self.data_type == "int":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "bool":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "float":
            glUniform1f(self.variable_ref, self.data)
        elif self.data_type == "vec2":
            glUniform2f(self.variable_ref, self.data[0], self.data[1])
        elif self.data_type == "vec3":
            glUniform3f(self.variable_ref, self.data[0], self.data[1],
                        self.data[2])
        elif self.data_type == "vec4":
            glUniform4f(self.variable_ref, self.data[0], self.data[1],
                        self.data[2], self.data[3])
        elif self.data_type == "mat4":
            # GL_TRUE if data is an array of row vectors
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, self.data)
