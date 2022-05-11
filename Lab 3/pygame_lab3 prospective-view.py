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
WIDTH, HEIGHT = 1000, 1000
screen_center = [WIDTH/2, HEIGHT/2]  # x, y
screen_center_vec = np.array([[WIDTH/2], [HEIGHT/2]])

pygame.display.set_caption("3D projection Lab#2")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# ============= Matrices ==================
def get_matrix_Rx(angle):
    rx = np.array([
        [1,             0,              0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle),  np.cos(angle), 0],
        [0,             0,              0, 1]])

    return rx


def get_matrix_Ry(angle):
    ry = np.array([
        [np.cos(angle) , 0,  np.sin(angle), 0],
        [0             , 1,              0, 0],
        [-np.sin(angle), 0,  np.cos(angle), 0],
        [0             , 0,              0, 1]])

    return ry


def get_matrix_Rz(angle):
    rz = np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle),  np.cos(angle), 0, 0],
        [0,             0,              1, 0],
        [0,             0,              0, 1]])

    return rz


def get_matrix_Tr(tx, ty, tz):
    translation_matrix = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]])
    return translation_matrix


# ============= Matruces INVERSE ==================
def get_matrix_RzInv(cos,sin):
    rz = np.array([
        [cos,  sin, 0, 0],
        [-sin, cos, 0, 0],
        [0,      0, 1, 0],
        [0,      0, 0, 1]])
    return rz


def get_matrix_RxInv(cos,sin):
    rx = np.array([
        [1,    0,   0, 0],
        [0,  cos, sin, 0],
        [0, -sin, cos, 0],
        [0,    0,   0, 1]])
    return rx


def get_matrix_RyInv(cos,sin):
    ry = np.array([
        [cos, 0, -sin, 0],
        [0,   1,    0, 0],
        [sin, 0,  cos, 0],
        [0,   0,    0, 1]])
    return ry


def get_matrix_TrInv(e, ty=0, tz=0):
    translation_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-e, -ty, -tz, 1]])
    return translation_matrix


def get_matrix_Scale(Sx, Sy, Sz):
    Scale_matrix = np.array([
        [Sx, 0, 0, 0],
        [0, Sy, 0, 0],
        [0, 0, Sz, 0],
        [0, 0, 0, 1]])
    return Scale_matrix


def get_matrix_S():
    Scale_matrix = np.array([
        [ 0, 1, 0, 0],
        [ 0, 0, 1, 0],
        [-1, 0, 0, 0],
        [ 0, 0, 0, 1]])
    return Scale_matrix



# ============= Functions ==================
def drawline_3d(point1, point2):
    # tuple1 = (point1.vec[0, 0], point1.vec[1, 0])
    # tuple2 = (point2.vec[0, 0], point2.vec[1, 0])
    pygame.draw.line(screen, BLACK, (point1.x,point1.y),\
        (point2.x, point2.y), width = 4)


def drawline_2d(point1, point2):
    # pygame.draw.line(screen, BLACK, (point1.x,point1.y),\
    #     (point2.x, point2.y), width=4)
    pygame.draw.line(screen, BLACK, (point1[0,0], point1[1,0]), \
        (point2[0,0], point2[1,0]), width=4)


# ============= Classes ==================
class Point():
    def __init__(self, x, y, z):
        self.vec = np.array([[x], [y], [z], [1]])
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        self.z = self.vec[2, 0]


    # def __add__(self, other_point):

    def vecprod(self, matrix):
        self.vec = matrix @ self.vec
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        self.z = self.vec[2, 0]

        return True

# print(Rz(np.pi/2)@a.vec)
class Wheel:
    def __init__(self, radius, height=0, x=0, y=0, z=0, color='black'):

        self.radius = radius
        self.height = height

        self.diag_coef = radius/np.sqrt(2)
        self.color = color

        self.center = Point(x, y, z)
        self.top = Point(x, y, height)

        self.circle_points = []
        self.circle_points.append( Point(self.center.x, self.center.y + self.radius, self.center.z ))
        self.circle_points.append( Point(self.center.x + self.diag_coef, self.center.y + self.diag_coef,\
            self.center.z))
        self.circle_points.append( Point(self.center.x + self.radius, self.center.y, self.center.z ))
        self.circle_points.append( Point(self.center.x + self.diag_coef, self.center.y - self.diag_coef,\
            self.center.z))
        self.circle_points.append( Point(self.center.x, self.center.y - self.radius, self.center.z ))
        self.circle_points.append( Point(self.center.x - self.diag_coef, self.center.y - self.diag_coef,\
            self.center.z))
        self.circle_points.append( Point(self.center.x - self.radius, self.center.y, self.center.z ))
        self.circle_points.append( Point(self.center.x - self.diag_coef, self.center.y + self.diag_coef,\
            self.center.z))

        self.points = list(self.circle_points)
        self.points.append(self.center)
        self.points.append(self.top)

    def translate_2_origin(self,):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(-cx, -cy, -cz))
        return True


    def translate(self, tx, ty, tz):
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(tx, ty, tz))
        return True

# ====================== Rotation ======================
    def rotate_x(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Rx(angle))
        self.translate(cx, cy, cz)
        return True

    def rotate_y(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Ry(angle))
        self.translate(cx, cy, cz)
        return True

    def rotate_z(self, angle):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Rz(angle))
        self.translate(cx, cy, cz)
        return True


# ====================== Project and draw ======================
class Camera:
    def __init__(self, xe=0, ye=0, ze=0, distance = 150):
        self.pos = (xe,ye,ze)
        self.v = np.sqrt(xe**2 + ye**2)
        self.e = np.sqrt(xe**2 + ye**2 + ze**2)
        self.cosTheta = xe/self.v
        self.sinTheta = ye/self.v
        self.cosPhi = ze/self.e
        self.sinPhi = self.v/self.e

        self.vrc_matrix = self.get_VRC_matrix()

        self.dist = distance
        self.proj_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0] ])


    def get_VRC_matrix(self,):
        matrix = get_matrix_RzInv(self.cosTheta, self.sinTheta) @ get_matrix_RyInv(self.cosPhi, self.sinPhi) @ \
            get_matrix_TrInv(self.e) @ get_matrix_S()
        return matrix

        # deg = 30
        # deg_rad = deg*np.pi/180
        # self.player_sc_dist = WIDTH/2/np.tan(deg_rad)


    def to_vrc(self, obj_3d):
        obj_3d.center_vrc = self.vrc_matrix @ obj_3d.center.vec
        obj_3d.top_vrc = self.vrc_matrix @ obj_3d.top.vec

        obj_3d.circle_vrc = []
        for i in range(len(obj_3d.circle_points)):
            p_vrc = self.vrc_matrix @ obj_3d.circle_points[i].vec
            obj_3d.circle_vrc.append(p_vrc)
        return True


    def proj_vrc(self, obj_3d):
        self.to_vrc(obj_3d)

        obj_3d.center_2d = self.proj_matrix @ obj_3d.center.vec + screen_center_vec
        obj_3d.top_2d = self.proj_matrix @ obj_3d.top.vec + screen_center_vec

        obj_3d.circle_2d = []
        for i in range(len(obj_3d.circle_points)):
            p_2d = self.proj_matrix @ obj_3d.circle_points[i].vec + \
                screen_center_vec
            obj_3d.circle_2d.append(p_2d)


    def draw(self, obj_2d):
        self.proj_vrc(obj_2d)
        for i in range(len(obj_2d.circle_2d)):
            drawline_2d(obj_2d.circle_2d[i], \
                     obj_2d.circle_2d[(i+1) % len(obj_2d.circle_2d)])
            drawline_2d(obj_2d.circle_2d[i], obj_2d.top_2d)




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
    w = Wheel(100, height=200, x=0, y=0)
    cam = Camera(xe=300, ye=300, ze=300)

    while True:
        # clock.tick(30)
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
        # print('transform1\n', w.center.vec == w.top.vec)
        # w.translate(5, 5, 0)
        cam.draw(w)
        w.rotate_x(0.001)
        w.rotate_y(0.001)
        w.rotate_z(0.001)

        # print('transform2\n', w.center.vec == w.top.vec)
        # w.translate_2_origin()

        # print('draw\n',w.center.vec == w.top.vec, '\n\n')
        # w.draw()


        pygame.display.update()

