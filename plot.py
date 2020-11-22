import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


class Plotter:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')

    def plot(self, Q):
        for i in range(1, Q.shape[0]):
            x = []
            y = []
            z = []
            for j in range(1, Q.shape[1]):
                q = max(Q[i, j, 0], Q[i, j, 1])
                x.append(i)
                y.append(j)
                z.append(q)
            self.ax.plot3D(x, y, z, 'gray')
            self.ax.scatter3D(x, y, z, marker='o')

    def clear(self):
        self.ax.clear()

    def show(self):
        plt.show()
