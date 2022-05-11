# ============= Imports ==================
from re import X
import pygame
import numpy as np
from pynput import keyboard  # using module keyboard

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
        [1, 0, 0, e],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
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
        [ 0, 0, 1, 0],
        [ 1, 0, 0, 0],
        [ 0, -1, 0, 0],
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


class Basis:
    def __init__(self,  x=0, y=0, z=0, color='red'):
        self.dd = 100
        self.points = []
        self.center = Point(x,y,z)
        self.points.append(Point(self.center.x + self.dd, y, z))
        self.points.append(self.center)
        self.points.append(Point(x,self.center.y + self.dd,z))
        self.points.append(self.center)
        self.points.append(Point(x,y,self.center.z + self.dd))



class Wheel:
    def __init__(self, radius, n=10, height=0, x=0, y=0, z=0, color='black'):
        self.n = n
        self.radius = radius
        self.height = height

        self.diag_coef = radius/np.sqrt(2)
        self.color = color

        self.center = Point(x, y, z)
        self.top = Point(x, y, height)

        self.points = self.get_circle_P()
        self.points.append(self.top)


    def get_circle_P(self,):
        unit_angle = 2*np.pi/self.n
        angle = 0
        points = []
        for i in range(self.n):
            dx = self.radius*np.cos(angle)
            dy = self.radius*np.sin(angle)
            points.append(Point(dx,dy,self.center.z))

            angle = angle + unit_angle
        return points

    def translate_2_origin(self,):
        cx, cy, cz = self.center.x, self.center.y, self.center.z
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(-cx, -cy, -cz))
        self.center.vecprod(get_matrix_Tr(-cx, -cy, -cz))
        return True


    def translate(self, tx, ty, tz):
        for i in range(len(self.points)):
            self.points[i].vecprod(get_matrix_Tr(tx, ty, tz))
        self.center.vecprod(get_matrix_Tr(tx, ty, tz))
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

    def get_proj_mx(self,vec):
        z = vec[2,0]
        # print(vec, ' = vec\n', z, ' = z\n')
        return np.array([
            [self.dist/z, 0, 0, 0],
            [0, self.dist/z, 0, 0]])

        # return np.array([
        #     [1, 0, 0, 0],
        #     [0, 1, 0, 0]])

    def get_VRC_matrix(self,):
        matrix = get_matrix_RzInv(self.cosTheta, self.sinTheta) @ \
            get_matrix_RyInv(self.cosPhi, self.sinPhi) @ \
            get_matrix_TrInv(self.e) @ get_matrix_S()
        return matrix


    def to_vrc(self, fig):
        fig.list_p_vrc = []
        for i in range(len(fig.points)):
            p_vrc = self.vrc_matrix @ fig.points[i].vec
            fig.list_p_vrc.append(p_vrc)

        print(fig.list_p_vrc[-1],'\n')
        return True


    def proj_vrc(self, fig):
        self.to_vrc(fig)

        fig.list_p_proj = []
        for i in range(len(fig.list_p_vrc)):
            p_2d = self.get_proj_mx(fig.list_p_vrc[i]) @ fig.list_p_vrc[i] + \
                screen_center_vec
            fig.list_p_proj.append(p_2d)
        return True


    def draw(self, fig):
        self.proj_vrc(fig)
        for i in range(len(fig.list_p_proj)):
            # print(i,'\n')
            # print(fig.list_p_proj[i],'\n----')
            n_points = len(fig.list_p_proj)-1
            drawline_2d(fig.list_p_proj[i], fig.list_p_proj[(i+1) % n_points])
            drawline_2d(fig.list_p_proj[i], fig.list_p_proj[-1])
        return True




if __name__ == '__main__':
    '''Main method'''



    translation = (0.00,0)
    rotation = 0.001

    # ============= Window and Draw ==================
    pygame.init()
    bg = pygame.Surface(screen.get_size())
    bg.fill((255, 255, 255))
    bg.convert()
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    screen.blit(bg, (0,0))

    # ============= Create object ==================
    w = Wheel(100, height=200, x=0, y=0)
    b = Basis()
    cam = Camera(xe=200, ye=200, ze=200, distance=200)

    while True:
        # clock.tick(5)
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
        # w.translate(0.05, 0, 0)
        # w.translate(0, 0.05, 0)
        # w.translate(0, 0, 0.05)

        cam.draw(w)
        # cam.draw(b)

        w.rotate_x(0.001)
        w.rotate_y(0.001)
        # w.rotate_z(0.001)

        # print('transform2\n', w.center.vec == w.top.vec)
        # w.translate_2_origin()

        # print('draw\n',w.center.vec == w.top.vec, '\n\n')
        # w.draw()


        pygame.display.update()

