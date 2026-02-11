#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

# kolory bazowe (definicja barwy swiatla)
base_light_ambient = [0.5, 0.5, 0.5, 1.0]
base_light_diffuse = [0.8, 0.8, 0.0, 1.0]
base_light_specular = [1.0, 1.0, 1.0, 1.0]

# aktualne intensywnosci (mnozniki) dla kazdej skladowej
# zakres od 0.0 do 1.0
ambient_intensity = 0.0
diffuse_intensity = 1.0
specular_intensity = 1.0

light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# tryby do wyboru: 1=ambient, 2=diffuse, 3=specular
current_light_param = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # ustawienie poczatkowe oswietlenia
    # funkcja render i tak nadpisze to w pierwszej klatce
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


# funkcja pomocnicza: mnozy kolor bazowy przez intensywnosc
def calculate_color(base, intensity):
    return [
        base[0] * intensity,
        base[1] * intensity,
        base[2] * intensity,
        base[3]
    ]


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    # aktualizacja parametrow swiatla w oparciu o aktualne intensywnosci
    glLightfv(GL_LIGHT0, GL_AMBIENT, calculate_color(base_light_ambient, ambient_intensity))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, calculate_color(base_light_diffuse, diffuse_intensity))
    glLightfv(GL_LIGHT0, GL_SPECULAR, calculate_color(base_light_specular, specular_intensity))

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    # zwiekszona dokladnosc sfery dla ladniejszego cieniowania
    gluSphere(quadric, 3.0, 20, 20)
    gluDeleteQuadric(quadric)

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


# funkcja modyfikujaca wybrana skladowa
def modify_light(change):
    global ambient_intensity, diffuse_intensity, specular_intensity

    if current_light_param == 1:
        ambient_intensity += change
        # ograniczenie do zakresu 0.0 - 1.0
        if ambient_intensity < 0.0: ambient_intensity = 0.0
        if ambient_intensity > 1.0: ambient_intensity = 1.0
        print(f"Ambient Intensity: {ambient_intensity:.1f}")

    elif current_light_param == 2:
        diffuse_intensity += change
        if diffuse_intensity < 0.0: diffuse_intensity = 0.0
        if diffuse_intensity > 1.0: diffuse_intensity = 1.0
        print(f"Diffuse Intensity: {diffuse_intensity:.1f}")

    elif current_light_param == 3:
        specular_intensity += change
        if specular_intensity < 0.0: specular_intensity = 0.0
        if specular_intensity > 1.0: specular_intensity = 1.0
        print(f"Specular Intensity: {specular_intensity:.1f}")


def keyboard_key_callback(window, key, scancode, action, mods):
    global current_light_param

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS:
        # wybor parametru
        if key == GLFW_KEY_1:
            current_light_param = 1
            print("Wybrano edycje: Ambient")
        elif key == GLFW_KEY_2:
            current_light_param = 2
            print("Wybrano edycje: Diffuse")
        elif key == GLFW_KEY_3:
            current_light_param = 3
            print("Wybrano edycje: Specular")

        # zmiana wartosci
        if key == GLFW_KEY_UP:
            modify_light(0.1)
        elif key == GLFW_KEY_DOWN:
            modify_light(-0.1)

    # obsluga przytrzymania klawisza dla plynnosci
    if action == GLFW_REPEAT:
        if key == GLFW_KEY_UP:
            modify_light(0.1)
        elif key == GLFW_KEY_DOWN:
            modify_light(-0.1)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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