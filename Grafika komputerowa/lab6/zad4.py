#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

viewer = [0.0, 0.0, 15.0]
theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

show_wall = True

current_texture_idx = 0
textures_ram = []  # Przechowywanie wczytanych tekstur w pamięci RAM

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def load_texture(filename):
    try:
        image = Image.open(filename)
        return {
            'width': image.size[0],
            'height': image.size[1],
            'data': image.tobytes("raw", "RGB", 0, -1)
        }
    except IOError:
        print(f"BŁĄD: Nie można odnaleźć pliku {filename}")
        sys.exit(1)


def update_gpu_texture(texture):
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, texture['width'], texture['height'], 0,
        GL_RGB, GL_UNSIGNED_BYTE, texture['data']
    )


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

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

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Wstępne wczytanie tekstur do pamięci RAM
    textures_ram.append(load_texture("moja_tekstura.tga"))
    textures_ram.append(load_texture("tekstura.tga"))

    # Ustawienie pierwszej tekstury
    update_gpu_texture(textures_ram[current_texture_idx])


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

    # Ściany boczne ostrosłupa
    glBegin(GL_TRIANGLES)

    # Ściana dolna
    glTexCoord2f(0.5, 0.5);
    glVertex3f(0.0, 0.0, 5.0)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0);
    glVertex3f(5.0, -5.0, 0.0)

    # Ściana prawa
    if show_wall:
        glTexCoord2f(0.5, 0.5);
        glVertex3f(0.0, 0.0, 5.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(5.0, -5.0, 0.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(5.0, 5.0, 0.0)

    # Ściana górna
    glTexCoord2f(0.5, 0.5);
    glVertex3f(0.0, 0.0, 5.0)
    glTexCoord2f(1.0, 1.0);
    glVertex3f(5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 1.0);
    glVertex3f(-5.0, 5.0, 0.0)

    # Ściana lewa
    glTexCoord2f(0.5, 0.5);
    glVertex3f(0.0, 0.0, 5.0)
    glTexCoord2f(0.0, 1.0);
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(-5.0, -5.0, 0.0)

    glEnd()

    # Podstawa (kwadrat)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(0.0, 1.0);
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(1.0, 1.0);
    glVertex3f(5.0, 5.0, 0.0)
    glTexCoord2f(1.0, 0.0);
    glVertex3f(5.0, -5.0, 0.0)
    glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global show_wall, current_texture_idx
    if action == GLFW_PRESS:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)

        # Przełączanie widoczności ściany
        if key == GLFW_KEY_SPACE:
            show_wall = not show_wall

        # Przełączanie tekstury klawiszem T
        if key == GLFW_KEY_T:
            current_texture_idx = (current_texture_idx + 1) % len(textures_ram)
            update_gpu_texture(textures_ram[current_texture_idx])


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
    glfwTerminate()


if __name__ == '__main__':
    main()