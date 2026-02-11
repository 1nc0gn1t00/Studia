#!/usr/bin/env python3
import sys
import math
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Konfiguracja Jajka
N = 20
egg_vertices = np.zeros((N, N, 3))
egg_normals = np.zeros((N, N, 3))

viewer = [0.0, 0.0, 15.0]

# Zmienne do obracania obiektem
theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

# Flaga wizualizacji wektorów
show_normals = False

# Materiał
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

# Światło (Statyczne)
light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def calculate_egg_data():
    # Oblicza wierzchołki i naprawione wektory normalne
    global egg_vertices, egg_normals

    u_vals = np.linspace(0, 1, N)
    v_vals = np.linspace(0, 1, N)

    for i in range(N):
        u = u_vals[i]
        for j in range(N):
            v = v_vals[j]

            # Współrzędne (x, y, z)
            P_u = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u)
            x = P_u * math.cos(math.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            z = P_u * math.sin(math.pi * v)
            egg_vertices[i][j] = [x, y, z]

            # Wektory normalne
            dP_du = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45)

            xu = dP_du * math.cos(math.pi * v)
            yu = 640 * u ** 3 - 960 * u ** 2 + 320 * u
            zu = dP_du * math.sin(math.pi * v)

            xv = math.pi * P_u * (-1) * math.sin(math.pi * v)
            yv = 0
            zv = math.pi * P_u * math.cos(math.pi * v)

            nx = yu * zv - zu * yv
            ny = zu * xv - xu * zv
            nz = xu * yv - yu * xv

            length = math.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
            if length == 0:
                length = 1
                nx, ny, nz = 0, 1, 0

            # Odwrócona logika względem poprzedniej wersji
            if i < N // 2:
                egg_normals[i][j] = [nx / length, ny / length, nz / length]
            else:
                egg_normals[i][j] = [-nx / length, -ny / length, -nz / length]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    calculate_egg_data()

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    # Rysowanie Jajka
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            glNormal3fv(egg_normals[i][j])
            glVertex3fv(egg_vertices[i][j])

            glNormal3fv(egg_normals[i + 1][j])
            glVertex3fv(egg_vertices[i + 1][j])

            glNormal3fv(egg_normals[i][j + 1])
            glVertex3fv(egg_vertices[i][j + 1])

            glNormal3fv(egg_normals[i + 1][j])
            glVertex3fv(egg_vertices[i + 1][j])

            glNormal3fv(egg_normals[i + 1][j + 1])
            glVertex3fv(egg_vertices[i + 1][j + 1])

            glNormal3fv(egg_normals[i][j + 1])
            glVertex3fv(egg_vertices[i][j + 1])
    glEnd()

    #  wizualizacja wektorów
    if show_normals:
        glDisable(GL_LIGHTING)  # Linie mają mieć własny kolor
        glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                v = egg_vertices[i][j]
                n = egg_normals[i][j]

                # Rysujemy linię od wierzchołka w stronę wskazywaną przez normalną
                glVertex3fv(v)
                glVertex3f(v[0] + n[0], v[1] + n[1], v[2] + n[2])
        glEnd()

        glEnable(GL_LIGHTING)  # Włączamy światło z powrotem

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, show_normals

    # Lewy przycisk: Obracanie
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            left_mouse_button_pressed = 1
        else:
            left_mouse_button_pressed = 0

    # Prawy przycisk: Przełączanie wizualizacji wektorów
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        show_normals = not show_normals
        print(f"Wizualizacja wektorów: {show_normals}")


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()