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

    draw_dywan_sierpinskiego(0.0, 0.0, 180.0, 90.0, 4)

    glFlush()


def draw_rectangle(x, y, a, b):
    x1, y1 = x - a / 2, y - b / 2  # lewy dół
    x2, y2 = x + a / 2, y - b / 2  # prawy dół
    x3, y3 = x + a / 2, y + b / 2  # prawy góra
    x4, y4 = x - a / 2, y + b / 2  # lewy góra

    glColor3f(0.55, 0.27, 0.07)
    glBegin(GL_TRIANGLES)
    # pierwszy trójkąt
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    # drugi trójkąt
    glVertex2f(x1, y1)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glEnd()


def draw_dywan_sierpinskiego(x, y, a, b, level):

    if level <= 0:
        draw_rectangle(x, y, a, b)
        return

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            x2 = x + i * a/3.0
            y2 = y + j * b/3.0
            draw_dywan_sierpinskiego(x2, y2, a/3.0, b/3.0, level - 1)


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