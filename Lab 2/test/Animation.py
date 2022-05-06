import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from celluloid import Camera

class Wheel:
    def __init__(self, canvas, radius, init_coordinates=(50, 50), color='black'):

        self.coordinates = init_coordinates
        self.radius = radius
        self.diag_coef = radius/np.sqrt(2)
        self.color = color
        self.canvas = canvas


    def draw(self,canvas_size=(8,8)):
        # plt.rcParams.update(
        #     {'font.size': 14, 'lines.markersize': 0, 'lines.linewidth': 2, 'axes.grid': False, 'lines.marker': 'o',})

        cx = self.coordinates[0]
        cy = self.coordinates[1]

        self.drawline(cx, cy, cx, cy + self.radius )
        self.drawline(cx, cy, cx, cy - self.radius )
        self.drawline(cx, cy, cx - self.radius , cy)
        self.drawline(cx, cy, cx + self.radius , cy)

        self.drawline(cx, cy, cx + self.diag_coef, cy + self.diag_coef)
        self.drawline(cx, cy, cx - self.diag_coef, cy + self.diag_coef)
        self.drawline(cx, cy, cx + self.diag_coef, cy - self.diag_coef)
        self.drawline(cx, cy, cx - self.diag_coef, cy - self.diag_coef)

        self.drawline(cx + self.radius , cy ,  cx + self.diag_coef, cy + self.diag_coef)
        self.drawline(cx + self.diag_coef, cy + self.diag_coef, cx , cy + self.radius)
        self.drawline(cx , cy + self.radius, cx - self.diag_coef, cy + self.diag_coef,)
        self.drawline(cx - self.radius , cy ,  cx - self.diag_coef, cy + self.diag_coef)

        self.drawline(cx - self.radius , cy,  cx - self.diag_coef, cy - self.diag_coef)
        self.drawline(cx - self.diag_coef, cy - self.diag_coef,  cx, cy - self.radius)
        self.drawline(cx, cy - self.radius,  cx + self.diag_coef, cy - self.diag_coef)
        # self.drawline(cx + self.diag_coef, cy - self.diag_coef, cx + self.radius, cy)


    def drawline(self, x1, y1, x2, y2, z1=0, z2=0):
        return self.canvas.plot([x1, x2], [y1, y2], [z1, z2],  marker='o',
                        linewidth=2, markersize=0, color=self.color)


canvas_size = (8,8)
plt.rcParams.update(
    {'font.size': 14, 'lines.markersize': 0, 'lines.linewidth': 2, 'axes.grid': False, 'lines.marker': 'o',})

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=canvas_size)

for ii in range(0, 360, 90):
    ax.view_init(elev=90., azim=ii)

# ====== Camera distance =======
depth = 10
ax.dist = depth

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
#ax.set_aspect('equal')
ax.axis('off')
camera = Camera(fig)

for i in range(50):
    w = Wheel(ax, 30, init_coordinates = (50+2*i,50-2*i) , color = "red")
    w.draw()
    camera.snap()
animation = camera.animate()
animation.save('celluloid_minimal.gif', writer = 'imagemagick')
