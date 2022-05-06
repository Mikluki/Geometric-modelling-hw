from re import X
import pygame
import numpy as np
# from math import *

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

# rotation_z = np.matrix([
#     [np.cos(angle), -np.sin(angle), 0],
#     [np.sin(angle), np.cos(angle), 0],
#     [0, 0, 1],
# ])

# rotation_y = np.matrix([
#     [np.cos(angle), 0, np.sin(angle)],
#     [0, 1, 0],
#     [-np.sin(angle), 0, np.cos(angle)],
# ])

# rotation_x = np.matrix([
#     [1, 0, 0],
#     [0, np.cos(angle), -np.sin(angle)],
#     [0, np.sin(angle), np.cos(angle)],
# ])
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

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

        p1 = Point(self.center.x, self.center.y+self.radius)
        p2 = Point(self.center.x+self.diag_coef, self.center.y+self.diag_coef)
        p3 = Point(self.center.x+self.radius, self.center.y)
        p4 = Point(self.center.x+self.diag_coef, self.center.y-self.diag_coef)
        p5 = Point(self.center.x, self.center.y-self.radius)
        p6 = Point(self.center.x-self.diag_coef, self.center.y-self.diag_coef)
        p7 = Point(self.center.x-self.radius, self.center.y)



        self.points = [p1,p2,p3,p4,p5,p6,p7]


    def draw(self):
        n = len(self.points)
        for i in range(n):
            drawline(self.points[i], (self.points[(i+1) % n]) )

# ============= Window and Draw ==================
clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff
    screen.fill(WHITE)
    Wee = Wheel(100, x=screen_center[0], y=screen_center[1])
    Wee.draw()

    # drawining stuff





    pygame.display.update()
