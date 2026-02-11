#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1, 1, 1, 1.0)


def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #wierzchołki trójkąta równobocznego
    v1 = (-90.0, -80.0)  # lewy dół
    v2 = (90.0, -80.0)  # prawy dół
    v3 = (0.0, 75.88)  # góra

    draw_sierpinski_triangle(v1, v2, v3, 4)

    glFlush()


def draw_triangle(v1, v2, v3):

    glColor3f(0.55, 0.27, 0.07)
    glBegin(GL_TRIANGLES)
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v3[0], v3[1])
    glEnd()


def draw_sierpinski_triangle(v1, v2, v3, level):

    if level <= 0:
        draw_triangle(v1, v2, v3)
        return

    # Środek boku v1-v2
    m1 = ((v1[0] + v2[0]) / 2.0, (v1[1] + v2[1]) / 2.0)
    # Środek boku v2-v3
    m2 = ((v2[0] + v3[0]) / 2.0, (v2[1] + v3[1]) / 2.0)
    # Środek boku v3-v1
    m3 = ((v3[0] + v1[0]) / 2.0, (v3[1] + v1[1]) / 2.0)

    # Dolny lewy trójkąt
    draw_sierpinski_triangle(v1, m1, m3, level - 1)

    # Dolny prawy trójkąt
    draw_sierpinski_triangle(m1, v2, m2, level - 1)

    # Górny trójkąt
    draw_sierpinski_triangle(m3, m2, v3, level - 1)


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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio,
                100.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio,
                -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Dywan Sierpińskiego", None, None)
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