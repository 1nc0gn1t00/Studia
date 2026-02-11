#!/usr/bin/env python3
import sys
import numpy as np
import time
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20
now = time.time()

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

def draw_pyramid(v):
    color = np.array([0.85, 0.65, 0.25])

    glBegin(GL_TRIANGLES)

    # Ściany boczne – różne odcienie
    # ściana 1
    glColor3fv(color * 1.0)
    glVertex3fv(v[0])
    glVertex3fv(v[1])
    glVertex3fv(v[4])

    # ściana 2
    glColor3fv(color * 0.8)
    glVertex3fv(v[1])
    glVertex3fv(v[2])
    glVertex3fv(v[4])

    # ściana 3
    glColor3fv(color * 0.6)
    glVertex3fv(v[2])
    glVertex3fv(v[3])
    glVertex3fv(v[4])

    # ściana 4
    glColor3fv(color * 0.4)
    glVertex3fv(v[3])
    glVertex3fv(v[0])
    glVertex3fv(v[4])

    # Podstawa – dzielimy kwadrat na dwa trójkąty
    glColor3fv(color * 0.2)
    glVertex3fv(v[0])
    glVertex3fv(v[1])
    glVertex3fv(v[2])

    glVertex3fv(v[0])
    glVertex3fv(v[2])
    glVertex3fv(v[3])

    glEnd()

def sierpinski_pyramid(v, depth):

    if depth == 0:
        draw_pyramid(v)
    else:
        # Wyznacz środki krawędzi podstawy
        m01 = (v[0] + v[1]) / 2
        m12 = (v[1] + v[2]) / 2
        m23 = (v[2] + v[3]) / 2
        m30 = (v[3] + v[0]) / 2
        center_base = (v[0] + v[1] + v[2] + v[3]) / 4
        top = v[4]

        # 4 dolne ostrosłupy przy rogach
        sierpinski_pyramid([v[0], m01, center_base, m30, (v[0] + top)/2], depth-1)
        sierpinski_pyramid([m01, v[1], m12, center_base, (v[1] + top)/2], depth-1)
        sierpinski_pyramid([center_base, m12, v[2], m23, (v[2] + top)/2], depth-1)
        sierpinski_pyramid([m30, center_base, m23, v[3], (v[3] + top)/2], depth-1)

        # 1 górny ostrosłup nad dolnymi
        # Podstawa: środki szczytów dolnych ostrosłupów (czyli punkty (v[i]+top)/2)
        b0 = (v[0] + top)/2
        b1 = (v[1] + top)/2
        b2 = (v[2] + top)/2
        b3 = (v[3] + top)/2
        sierpinski_pyramid([b0, b1, b2, b3, top], depth-1)



def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / np.pi)
    #axes()

    # Początkowy ostrosłup czworokątny
    size = 4.0
    v0 = np.array([-size, -size, -size])
    v1 = np.array([size, -size, -size])
    v2 = np.array([size, -size, size])
    v3 = np.array([-size, -size, size])
    v4 = np.array([0.0, size, 0.0])  # szczyt

    DEPTH = 3

    sierpinski_pyramid([v0, v1, v2, v3, v4], DEPTH)

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
