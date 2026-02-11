#!/usr/bin/env python3
import sys
import math
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

# Parametry modelu jajka
N = 40
egg_vertices = np.zeros((N, N, 3))
egg_uv = np.zeros((N, N, 2))

viewer = [0.0, 0.0, 15.0]
theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.2, 0.2, 0.2, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]


def calculate_egg():
    global egg_vertices, egg_uv
    u_vals = np.linspace(0, 1, N)
    v_vals = np.linspace(0, 1, N)

    for i in range(N):
        u = u_vals[i]
        for j in range(N):
            v = v_vals[j]

            P_u = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u)
            x = P_u * math.cos(math.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
            z = P_u * math.sin(math.pi * v)

            egg_vertices[i][j] = [x, y, z]
            egg_uv[i][j] = [u * 4, v]


def startup():
    update_viewport(None, 600, 600)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    calculate_egg()

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glDisable(GL_CULL_FACE)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Ustawienie powtarzania tekstury, żeby v*2 nie ucinało obrazu
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    try:
        image = Image.open("moja_tekstura.tga")
        glTexImage2D(GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
                     GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1))
    except IOError:
        sys.exit(1)


def render(time):
    global theta, phi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    glTranslatef(0.0, -5.0, 0.0)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glTexCoord2fv(egg_uv[i][j])
            glVertex3fv(egg_vertices[i][j])
            glTexCoord2fv(egg_uv[i + 1][j])
            glVertex3fv(egg_vertices[i + 1][j])
        glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    if width == 0: width = 1
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old
    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    if button == GLFW_MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = 1 if action == GLFW_PRESS else 0


def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(600, 600, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()


if __name__ == '__main__':
    main()