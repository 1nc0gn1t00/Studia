#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    draw_rectangle(0.0, 0.0, 80.0, 40.0)  # prostokąt na środku

    glFlush()

def draw_rectangle(x, y, a, b):

    # Wierzchołki (wokół środka)
    x1, y1 = x - a/2, y - b/2  # lewy dół
    x2, y2 = x + a/2, y - b/2  # prawy dół
    x3, y3 = x + a/2, y + b/2  # prawy góra
    x4, y4 = x - a/2, y + b/2  # lewy góra

    # Pierwszy trójkąt:
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x1, y1)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x2, y2)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x3, y3)
    glEnd()

    # Drugi trójkąt:
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x3, y3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x4, y4)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x1, y1)
    glEnd()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()