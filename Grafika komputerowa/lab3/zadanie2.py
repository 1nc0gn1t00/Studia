#!/usr/bin/env python3
import sys
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 30

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def draw_egg():
    # tworzy pustą macierz o wymiarach NxNx3
    tab = np.zeros((N, N, 3))

    # u odpowiada za wysokość jajka, v za obrót wokół osi Y
    u, v = np.linspace(0, 1, N), np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            x = (-90 * u[i] ** 5 + 225 * u[i] ** 4 - 270 * u[i] ** 3 + 180 * u[i] ** 2 - 45 * u[i]) * np.cos(np.pi * v[j])
            y = 160 * u[i] ** 4 - 320 * u[i] ** 3 + 160 * u[i] ** 2
            z = (-90 * u[i] ** 5 + 225 * u[i] ** 4 - 270 * u[i] ** 3 + 180 * u[i] ** 2 - 45 * u[i]) * np.sin(np.pi * v[j])
            tab[i][j] = [x, y - 5, z]  # przesuwamy jajko lekko w dół (żeby środek był w osi)

    #rysowanie siatki z linii
    glBegin(GL_LINES)
    glColor3f(1, 0, 0.5)
    for i in range(N-1):
        for j in range(N-1):
            # linia pionowa (po u)
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i + 1][j])

            # linia pozioma (po v)
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i][j + 1])
    glEnd()



def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    draw_egg()

    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
