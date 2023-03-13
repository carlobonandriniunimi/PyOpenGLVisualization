from OpenGL.GL import *
import numpy


class Attribute:
    def __init__(self, data_type, data):
        # type of elements in data array:
        # int | float | vec2 | vec3 | vec4
        self.data_type = data_type

        # array of data to be stored in buffer
        self.data = data

        # reference of available buffer from GPU
        self.buffer_ref = glGenBuffers(1)

        # upload data immediately
        self.upload_data()

    def upload_data(self):
        """Upload this data to a GPU buffer."""
        # convert data to numpy array format
        # convert numbers to 32-bit floats
        data = numpy.array(self.data, dtype=numpy.float32)

        # select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)

        # store data in currently bound buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associate_variable(self, program_ref, variable_name):
        """Associate variable in program with this buffer."""
        # get reference for program variable with given name
        variable_ref = glGetAttribLocation(program_ref, variable_name)

        # if the program does not reference the variable then exit
        if variable_ref == -1:
            return

        # select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)

        # specify how data will be read from the currently bound buffer
        # into the specified variable
        if self.data_type == 'int':
            glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == 'float':
            glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec2':
            glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec3':
            glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec4':
            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception("Attribute " + variable_name + " has unknown type " +
                            self.data_type)

        # indicate that data will be streamed to this variable
        glEnableVertexAttribArray(variable_ref)
