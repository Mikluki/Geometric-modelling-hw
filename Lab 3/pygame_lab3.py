# ============= Imports ==================
from re import X
import pygame
import numpy as np
from pynput import keyboard  # using module keyboard
# from math import *

direction = 0

def on_press(key):
    global direction
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if key.char == "a":
            direction = 0
        elif key.char == "d":
            direction = 1
        elif key.char == "w":
            direction = 2
        elif key.char == "s":
            direction = 3
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

scale = 100
WIDTH, HEIGHT = 1000, 800
screen_center = [WIDTH/2, HEIGHT/2]  # x, y

pygame.display.set_caption("3D projection Lab#2")
screen = pygame.display.set_mode((WIDTH, HEIGHT))



points = []
p1 = np.matrix([-1, -1, 1])
p2 = np.matrix([1, -1, 1])

# ============= Matrices ==================

# matrix = np.matrix([
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1]])

projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])


def get_matrix_Rx(angle):
    rx = np.matrix([
        [1,             0,              0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle),  np.cos(angle), 0],
        [0,             0,              0, 1]])

    return rx


def get_matrix_Ry(angle):
    ry = np.matrix([
        [np.cos(angle),             0,  np.sin(angle), 0],
        [0            ,             1,              0, 0],
        [-np.sin(angle),            0,  np.cos(angle), 0],
        [0            ,             0,              0, 1]])

    return ry


def get_matrix_Rz(angle):
    rz = np.matrix([
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle),  np.cos(angle), 0],
        [0,             0,              1, 0],
        [0,             0,              0, 1]])

    return rz


def get_matrix_Tr(tx, ty, tz):
    translation_matrix = np.matrix([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]])
    return translation_matrix

# ============= Functions ==================
def drawline(point1, point2):
    # tuple1 = (point1.vec[0, 0], point1.vec[1, 0])
    # tuple2 = (point2.vec[0, 0], point2.vec[1, 0])
    pygame.draw.line(screen, BLACK, (point1.x,
                        point1.y), (point2.x, point2.y), width = 4)


# ============= Classes ==================
class Point():
    def __init__(self, x, y, z):
        self.vec = np.matrix([[x], [y], [z], [1]])
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        self.z = self.vec[2, 0]


    # def __add__(self, other_point):

    def vecprod(self, matrix):
        self.vec = matrix @ self.vec
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        if len(self.vec) >= 3:
            self.z = self.vec[2, 0]

        return self

# print(Rz(np.pi/2)@a.vec)
class Wheel:
    def __init__(self, radius, x=0, y=0, z=0, color='black'):

        self.radius = radius
        self.diag_coef = radius/np.sqrt(2)
        self.color = color

        self.center = Point(x, y, z)
        self.cirle_points = []
        self.cirle_points.append( Point(self.center.x, self.center.y + self.radius, self.center.z ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y + self.diag_coef,\
            self.center.z))
        self.cirle_points.append( Point(self.center.x + self.radius, self.center.y, self.center.z ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y - self.diag_coef,\
            self.center.z))
        self.cirle_points.append( Point(self.center.x, self.center.y - self.radius, self.center.z ))
        self.cirle_points.append( Point(self.center.x - self.diag_coef, self.center.y - self.diag_coef,\
            self.center.z))
        self.cirle_points.append( Point(self.center.x - self.radius, self.center.y, self.center.z ))
        self.cirle_points.append( Point(self.center.x - self.diag_coef, self.center.y + self.diag_coef,\
            self.center.z))

        self.points = list(self.cirle_points)
        self.points.append(self.center)


    def translate_2_origin(self,):
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(-self.center.x, -self.center.y, -self.center.z))
        return self

    def translate(self, tx, ty, tz):
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(tx, ty, tz))
        return self

# ====================== Rotation ======================
    def rotate_x(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Rx(angle))
        self.translate(cx, cy, cz)
        return self

    def rotate_y(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Ry(angle))
        self.translate(cx, cy, cz)
        return self

    def rotate_z(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Rz(angle))
        self.translate(cx, cy, cz)
        return self


# ====================== Priject and draw ======================
    def project_to_screen(self):
        for i in range(len(self.points)):
            # print(self.points[i].vec, 'mult to\n', projection_matrix, '  n={}\n\n'.format(i))
            projection2d = projection_matrix @ self.points[i].vec
        return projection2d


    def draw(self):
        self.project_to_screen()
        for i in range(len(self.cirle_points)):
            drawline(self.points[i], (self.points[(i+1) % len(self.cirle_points)]))
            drawline(self.points[i], (self.center))



if __name__ == '__main__':
    '''Main method'''


    # # Keyboard:
    # # Collect events until released
    # listener = keyboard.Listener(
    #     on_press=on_press,
    #     on_release=on_release)
    # listener.start()

    FPS = 30

    translation = (0.00,0)
    rotation = 0.001

    # ============= Window and Draw ==================
    pygame.init()
    bg = pygame.Surface(screen.get_size())
    bg.fill((255, 255, 255))
    bg.convert()
    clock = pygame.time.Clock()
    milliseconds = clock.tick(FPS)
    screen.fill(WHITE)
    screen.blit(bg, (0,0))

    # ============= Create object ==================
    w = Wheel(100, x=screen_center[0], y=screen_center[1])

    while True:
        screen.blit(bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # update stuff
        # w.translate(*translation)
        w.rotate_x(0.001)
        w.rotate_y(0.002)
        # w.rotate_z(0.001)


        w.draw()


        pygame.display.update()

