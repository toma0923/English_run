import numpy as np
import bokeh.plotting as bkplt

fig = bkplt.figure(frame_width=300, frame_height=300, match_aspect=True)
fig.dot([0, 1], [0, 1], visible=False)  # WORKAROUND

num_points = 10_000    # 危険!!: 絶対に 40_000 を超えないこと．

rng = np.random.default_rng()
data = rng.random(size=(2, num_points))
# print(data[:])

cols_pass = data[1, :] < (1 + np.cos(5 * np.pi * data[0, :])) / 4
# print(cols_pass)
x_pass, y_pass = data[:, np.ndarray([1, 0, 1, 0])]
print(type(cols_pass))
print(x_pass, y_pass)
fig.dot(x_pass, y_pass, color='blue', size=8)

cols_fail = np.logical_not(cols_pass)
# print(cols_fail)
x_fail, y_fail = data[:, cols_fail]
fig.dot(x_fail, y_fail, color='red', size=8)
