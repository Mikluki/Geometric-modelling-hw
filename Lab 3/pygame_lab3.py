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
WIDTH, HEIGHT = 800, 600
screen_center = [WIDTH/2, HEIGHT/2]  # x, y

pygame.display.set_caption("3D projection Lab#2")
screen = pygame.display.set_mode((WIDTH, HEIGHT))



points = []
p1 = np.matrix([-1, -1, 1])
p2 = np.matrix([1, -1, 1])

# # all the cube vertices
# points.append(np.matrix([-1, -1, 1]))
# points.append(np.matrix([1, -1, 1]))
# points.append(np.matrix([1,  1, 1]))
# points.append(np.matrix([-1, 1, 1]))
# points.append(np.matrix([-1, -1, -1]))
# points.append(np.matrix([1, -1, -1]))
# points.append(np.matrix([1, 1, -1]))
# points.append(np.matrix([-1, 1, -1]))

# ============= Matrices ==================


# rotation_y = np.matrix([
#     [np.cos(angle), 0, np.sin(angle)],
#     [0, 1, 0],
#     [-np.sin(angle), 0, np.cos(angle)],
# ])

# matrix = np.matrix([
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1]])

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


def rotation_matrix(angle):
    rotation_matrix = np.matrix([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]])

    return rotation_matrix


def translation_matrix(tx, ty):
    translation_matrix = np.matrix([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]])
    return translation_matrix

# ============= Functions ==================
def drawline(point1, point2):
    # tuple1 = (point1.vec[0, 0], point1.vec[1, 0])
    # tuple2 = (point2.vec[0, 0], point2.vec[1, 0])
    pygame.draw.line(screen, BLACK, (point1.x,
                        point1.y), (point2.x, point2.y), width = 4)


# ============= Classes ==================
class Point():
    def __init__(self, x, y):
        self.vec = np.matrix([[x], [y], [1]])
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]

    # def __add__(self, other_point):

    def vecprod(self, matrix):
        self.vec = matrix @ self.vec
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        return self


class Wheel:
    def __init__(self, radius, x=screen_center[0], y=screen_center[1], color='black'):

        self.radius = radius
        self.diag_coef = radius/np.sqrt(2)
        self.color = color

        self.center = Point(x, y)
        self.cirle_points = []
        self.cirle_points.append( Point(self.center.x, self.center.y + self.radius ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y + self.diag_coef))
        self.cirle_points.append( Point(self.center.x + self.radius, self.center.y ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y - self.diag_coef))
        self.cirle_points.append( Point(self.center.x, self.center.y - self.radius ))
        self.cirle_points.append( Point(self.center.x - self.diag_coef, self.center.y - self.diag_coef))
        self.cirle_points.append( Point(self.center.x - self.radius, self.center.y ))
        self.cirle_points.append( Point(self.center.x - self.diag_coef, self.center.y + self.diag_coef))

        self.points = list(self.cirle_points)
        self.points.append(self.center)

        #self.cirle_points.append(  )

    def translate_2_origin(self,):
        for i in range(len(self.points)):
            self.points[i].vecprod(
                translation_matrix(-self.center.x, -self.center.y))
        return self

    def translate(self, tx, ty):
        for i in range(len(self.points)):
            self.points[i].vecprod(translation_matrix(tx,ty))
        return self

    def rotate(self, angle):
        cx, cy = self.center.x, self.center.y
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(rotation_matrix(angle))
        self.translate(cx, cy)
        return self



    def draw(self):
        for i in range(len(self.cirle_points)):
            drawline(self.points[i], (self.points[(i+1) % len(self.cirle_points)]))
            drawline(self.points[i], (self.center))


if __name__ == '__main__':
    '''Main method'''


    # Keyboard:
    # Collect events until released
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    FPS = 30

    translation = (0.00,0)
    rotation = 0.000

    # ============= Window and Draw ==================
    pygame.init()
    bg = pygame.Surface(screen.get_size())
    bg.fill((255, 255, 255))
    bg.convert()
    clock = pygame.time.Clock()
    milliseconds = clock.tick(FPS)
    screen.fill(WHITE)
    screen.blit(bg, (0,0))

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
        w.translate(*translation)
        w.rotate(rotation)

        w.draw()
        #print(f"Direction = {direction}")
        if direction == 0:
            translation = (-0.2,0)
            rotation = - 0.001
        if direction == 1:
            translation = (0.2,0)
            rotation =  0.001
        if direction == 2:
            translation = (0,-0.2)
            rotation = 0
        if direction == 3:
            translation = (0.0,0.2)
            rotation = 0



        pygame.display.update()
