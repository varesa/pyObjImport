import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo

import numpy

import objImporter

class Render:
    def __init__(self):
        pass

    def init(self):
        display = pygame.display.set_mode((800, 600), HWSURFACE | OPENGL | DOUBLEBUF)

        vertex_shader = shaders.compileShader("""
        #version 130

        void main() {
            gl_TexCoord[0] = gl_MultiTexCoord0;
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
        """, GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""
        #version 130

        uniform sampler2D texture;

        void main() {
            //gl_FragColor = vec4(1, 0, 0, 0);
            gl_FragColor = texture2D(texture, gl_TexCoord[0].st);
        }
        """, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

        """self.vbo = vbo.VBO(
            numpy.array([
                [-1, -1, 0],
                [-1, 1, 0],
                [1, 1, 0]
            ], 'f')
        )"""

        imp = objImporter.Importer()
        imp.open("/home/esa/test.obj")
        arr = numpy.array(imp.getArray(), 'f')
        self.size = len(arr)
        self.vbo = vbo.VBO(arr)

        print(imp.getMaterial().map_Kd)

        img = pygame.image.load("/home/esa/" + imp.getMaterial().map_Kd)
        imgData = pygame.image.tostring(img, "RGBA", 1)


        self.texId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0 , GL_RGBA, GL_UNSIGNED_BYTE, imgData)

        glClearColor(1, 1, 1, 0)

    stop = False

    def main(self):
        self.init()

        mouse = False
        lastx = None
        lasty = None

        x_rot = 0
        y_rot = 0

        while not self.stop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop = True
                if event.type == MOUSEBUTTONDOWN:
                    mouse = True
                    lastx = pygame.mouse.get_pos()[0]
                    lasty = pygame.mouse.get_pos()[1]
                if event.type == MOUSEBUTTONUP:
                    mouse = False
                if event.type == MOUSEMOTION:
                    if mouse:
                        xdiff = event.pos[0] - lastx
                        ydiff = event.pos[1] - lasty

                        y_rot += ydiff

                        if y_rot < 90 or y_rot > 270:
                            x_rot += xdiff
                        else:
                            x_rot -= xdiff

                        if x_rot > 360:
                            x_rot -= 360
                        if x_rot < 0:
                            x_rot += 360

                        if y_rot > 360:
                            y_rot -= 360
                        if y_rot < 0:
                            y_rot += 360

                        lastx = event.pos[0]
                        lasty = event.pos[1]


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glMatrixMode(GL_PROJECTION)

            glLoadIdentity()
            gluPerspective(90, 800/600.0, 0.1, 100)
            gluLookAt(0,0, 5, 0, 0, 0, 0, 1, 0)

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glRotatef(x_rot, 0, 1, 0)

            if x_rot < 90:
                glRotatef(y_rot, 1-x_rot/90.0, 0, x_rot/90.0)
            elif x_rot < 180:
                t = x_rot - 90
                glRotatef(y_rot, -t/90.0, 0, 1-t/90.0)
            elif x_rot < 270:
                t = x_rot - 180
                glRotatef(y_rot, -1+t/90.0, 0, -t/90.0)
            else:
                t = x_rot - 270
                glRotatef(y_rot, t/90.0, 0, -1+t/90.0)


            glUseProgram(self.shader)

            texture_location = glGetUniformLocation(self.shader, "texture")
            glUniform1i(texture_location, 0)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texId)

            glShadeModel(GL_FLAT)

            try:
                self.vbo.bind()
                try:
                    glEnableClientState(GL_VERTEX_ARRAY)

                    glVertexPointer(3, GL_FLOAT, 32, self.vbo)
                    glTexCoordPointer(2, GL_FLOAT, 32, self.vbo+12)
                    glNormalPointer(GL_FLOAT, 32, self.vbo+20)
                    glDrawArrays(GL_TRIANGLES, 0, self.size)
                finally:
                    glDisableClientState(GL_VERTEX_ARRAY)
                    self.vbo.unbind()
            finally:
                glUseProgram(0)

            pygame.display.flip()


if __name__ == "__main__":
    r = Render()
    r.main()