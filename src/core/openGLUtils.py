from OpenGL.GL import *


# static methods to load adn compile OpenGL shaders
# and link to create programs
class OpenGLUtils:
    @staticmethod
    def print_system_info():
        print(" Vendor: " + glGetString(GL_VENDOR).decode('utf-8'))
        print("Renderer: " + glGetString(GL_RENDERER).decode('utf-8'))
        print("OpenGL version supported: " +
              glGetString(GL_VERSION).decode('utf-8'))
        print(" GLSL version supported: " +
              glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8'))

    @staticmethod
    def initialize_shader(shader_code, shader_type):
        # specify required OpenGL/GLSL version
        shader_code = '#version 330\n' + shader_code

        # create empty shader object and return ref value
        shader_ref = glCreateShader(shader_type)
        # stores the source code in the shader
        glShaderSource(shader_ref, shader_code)
        # compiles source code
        glCompileShader(shader_ref)

        # queries whether shader compile was successful
        compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
        if not compile_success:
            # retrieve error message
            error_message = glGetShaderInfoLog(shader_ref)
            # free memory used to store the shader
            glDeleteShader(shader_ref)
            # convert byte string to char string
            error_message = '\n' + error_message.decode('utf-8')
            # raise exception: halt program and print error
            raise Exception(error_message)

        # compilation was successful; return shader ref value
        return shader_ref

    @staticmethod
    def initialize_program(vertex_shader_code, fragment_shader_code):
        # compile vertex and fragment shaders
        vertex_shader_ref = OpenGLUtils.initialize_shader(
            vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader_ref = OpenGLUtils.initialize_shader(
            fragment_shader_code, GL_FRAGMENT_SHADER)

        # create empty program object and store ref
        program_ref = glCreateProgram()

        # attach previously compiled shader programs
        glAttachShader(program_ref, vertex_shader_ref)
        glAttachShader(program_ref, fragment_shader_ref)

        # link vertex shader to fragment shader
        glLinkProgram(program_ref)

        # queries whether program link was successful
        link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)
        if not link_success:
            # retrieve error message
            error_message = glGetProgramInfoLog(program_ref)
            # free memory used to store program
            glDeleteProgram(program_ref)
            # convert byte string to char string
            error_message = '\n' + error_message.decode('utf-8')
            # raise exception and print error
            raise Exception(error_message)

        # linking was successful, return program ref
        return program_ref
