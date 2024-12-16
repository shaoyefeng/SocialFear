import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection

colorbar_font_size = 5
r = 4
l = 2

def triangle_for_vector(x, y, px, py, r):  # r=4
    return ((px + y / r) - x, (py - x / r) - y), ((px - y / r) - x, (py + x / r) - y), ((px + x), (py + y))


def triangle_for_angle(a, px, py, l, r):  # l=0.5
    return triangle_for_vector(np.cos(np.deg2rad(a)) * l, np.sin(np.deg2rad(a)) * l, px, py, r)


def points_to_line_collection(xs, ys, cmap, linewidth):
    points = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    t = np.arange(0, len(segments))
    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(t[::-1])  # t
    lc.set_linewidth(linewidth)
    return lc


g_colorbar = {}
def plot_colorbar(ax, tmin=None, tmax=None, im=None, inter=1):
    # global g_colorbar
    # if g_colorbar.get(ax):
    #     g_colorbar[ax].remove()
    #shrink = 0.3, aspect = 10
    # axes = plt.axes()
    g_colorbar[ax] = plt.colorbar(im, ax=ax, label='frame')
    cax = g_colorbar[ax].ax
    yax = cax.yaxis
    yax.set_ticks([0, 1])
    yax.set_ticklabels([tmax*inter, tmin])

    # if vmin is not None:
    #     yax.set_ticks([vmin, vmax])
    #     if 0 <= vmin and vmax <= 1:
    #         yax.set_ticklabels(["%.1f%%" % (vmin * 100), "%.1f%%" % (vmax * 100)])
    #     elif vmax <= 30:
    #         yax.set_ticklabels([str(vmin), str(vmax)])
    #         g_colorbar[ax].set_label("mm/s", fontsize=colorbar_font_size)
    #     else:
    #         yax.set_ticklabels([str(vmin) + "°", str(vmax) + "°"])
    for l in yax.get_ticklabels():
        l.set_fontsize(colorbar_font_size)


def plot_overlap_time(ax, xs, ys, dirs, fly, inter=10):
    # xs, ys, dirs = filter_wrong_pos(xs, ys, dirs)
    a_l = np.arange(1, 0.001, -1 / len(xs)) * 0.9
    color = 'b'
    if fly == 1:
        color_l = [(a, a, 1) for a in a_l]
    else:
        color_l = [(1, a, a) for a in a_l]
    alpha_l = 1 - a_l
    ax.scatter(xs, ys, linewidth=1, color=color_l, marker=".")
    for j in range(1, len(xs)):
        line = plt.Line2D(xs[j - 1:j + 1], ys[j - 1:j + 1], color=color_l[j])
        ax.add_line(line)
    j = 0
    for x, y in zip(xs, ys):
        if j % inter == 0:
            d = dirs.iloc[j]
            rect = plt.Polygon(triangle_for_angle(d, x, y, l, r), color=color, alpha=alpha_l[j], linewidth=0)  # 0.5
            ax.add_patch(rect)
        j += 1


def plot_overlap_time2(ax, xs, ys, dirs, fly, inter, need_colorbar=False, cmap=None):
    xs, ys, dirs = xs.tolist(), ys.tolist(), dirs.tolist()
    if not cmap:
        cmap = "viridis"
    ax.add_collection(points_to_line_collection(xs, ys, cmap, 2))

    verts = []
    j = 0
    for x, y in zip(xs, ys):
        if j % inter == 0:
            d = dirs[j]
            verts.append(triangle_for_angle(d, x, y, l, r))
        j += 1
    t = np.arange(0, len(verts))
    norm = plt.Normalize(t.min(), t.max())
    pc = PolyCollection(verts, cmap=cmap, norm=norm, alpha=1)
    pc.set_array(t[::-1]) #t
    ax.add_collection(pc)
    need_colorbar and plot_colorbar(ax, t.min(), t.max(), im=pc, inter=inter)

# heatmap
# xbins = np.arange(0, 450, 1)
# ybins = np.arange(0, 20.1, 0.1)
# plt.hist2d(x, y, bins=[xbins, ybins])
# plt.colorbar()

# df_statistics = block_df['posy'].groupby(block_df['frame']).agg(['mean', 'std'])
# x = df_statistics['frame']
# y = df_statistics['mean']
# err = df_statistics['std']
# plt.plot(x, y, color='blue', alpha=0.4)
# plt.fill_between(x, y + err, y - err, alpha=0.1, color='blue')
# plt.show()