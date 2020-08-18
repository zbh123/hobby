import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 指定渲染环境
# %matplotlib notebook
# %matplotlib inline

# x = np.linspace(0, 2 * np.pi, 100)
# y = np.sin(x)
# fig = plt.figure(tight_layout=True)
# plt.plot(x, y)
# plt.grid(ls='--')
# plt.show()


def update_points(num):
    point_ani.set_data(x[num], y[num])
    return point_ani,


x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig = plt.figure(tight_layout=True)
plt.plot(x, y)
point_ani, = plt.plot(x[0], y[0], 'ro')
plt.grid(ls='--')
ani = animation.FuncAnimation(fig, update_points, np.arange(0, 100), interval=100, blit=True)
# plt.show()


def update_points1(num):
    if num % 5 == 0:
        point_ani1.set_marker("*")
        point_ani1.set_markersize(12)
    else:
        point_ani1.set_marker('o')
        point_ani1.set_markersize(8)
    point_ani1.set_data(x[num], y[num])
    text_pt.set_text('x=%.3f, y=%.3f' % (x[num], y[num]))
    return point_ani1, text_pt


fig = plt.figure(tight_layout=True)
plt.plot(x, y)
point_ani1, = plt.plot(x[0], y[0], 'ro')
plt.grid(ls='--')
text_pt = plt.text(4, 0.8, '', fontsize=16)
ani1 = animation.FuncAnimation(fig, update_points1, np.arange(0, 100), interval=100, blit=True)
# plt.show()


def update_points2(num):
    if num % 5 == 0:
        point_ani2.set_marker("*")
        point_ani2.set_markersize(12)
    else:
        point_ani2.set_marker('o')
        point_ani2.set_markersize(8)
    text_pt1.set_position((x[num], y[num]))
    text_pt1.set_text('x=%.3f, y=%.3f' % (x[num], y[num]))
    return point_ani2, text_pt1


fig = plt.figure(tight_layout=True)
plt.plot(x, y)
point_ani2, = plt.plot(x[0], y[0], 'ro')
plt.grid(ls='--')
text_pt1 = plt.text(4, 0.8, '', fontsize=16)
ani2 = animation.FuncAnimation(fig, update_points2, np.arange(0, 100), interval=100, blit=True)
plt.show()

