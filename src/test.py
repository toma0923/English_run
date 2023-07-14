import numpy as np

# 重りを入力(単位はmm)
M = np.array([0, 199.975, 199.972, 199.973, 199.985, 199.975, 199.99, 199.98])*10**-3

# 幅（3つ）を入力(単位はmm)
w_av = np.array([16.0, 15.9, 16.0])*10**-3

# 高さ（3つ）を入力(単位はmm)
t_av = np.array([4.97, 4.9, 5.03])*10**-3

# 傾きを入力
k = 0.06138995988


# dを入力(単位はcm)
d = 3.25 * 10**-2

# Lを入力(単位はcm)
L = 40.0 * 10**-2

# 重力加速度
g = 9.78

# Dを入力(単位はm)
D_1 = 1.15
D_2 = 1.15


dY_f_u = np.array([30 ,28.7, 27.6, 26.5, 25.1, 23.8, 22.6, 21.5]) * 10 ** -2  # 上り
dY_f_d = np.array([30 ,28.6, 27.5, 26.2, 25.1, 23.8, 22.6, 21.5]) * 10 ** -2  # 下り
dY_b_u = np.array([30 ,28.5, 27.2, 26.0, 24.7, 23.5, 22.2, 21.0]) * 10 ** -2  # 上り
dY_b_d = np.array([29.7 ,28.4, 27.2, 26.0, 24.6, 23.5, 22.2, 21.0]) * 10 ** -2  # 下り

# ここからは入力しなくてよい

w = (w_av[0] + w_av[1] + w_av[2]) / 3

t = (t_av[0] + t_av[1] + t_av[2]) / 3

D = (D_1 + D_2) / 2

dY_A = np.zeros(7)  # dY_A の結果を格納する配列を初期化
dY = np.zeros(7)  # dY の結果を格納する配列を初期化
for i in range(0, 7):
    if i == 0:
        dY_A[i] = (abs(dY_f_u[i] - dY_f_u[i + 1]) + abs(dY_f_d[i] - dY_f_d[i + 1])) + (
                abs(dY_b_u[i] - dY_b_u[i + 1]) + abs(dY_b_d[i] - dY_b_d[i + 1]))
        dY[i] = dY_A[i] / 4
        print(f'dY[i+1] = {dY[i]}')

    else:
        dY_A[i] = (abs(dY_f_u[i] - dY_f_u[i + 1]) + abs(dY_f_d[i] - dY_f_d[i + 1])) + (
                abs(dY_b_u[i] - dY_b_u[i + 1]) + abs(dY_b_d[i] - dY_b_d[i + 1]))
        dY[i] = dY[i - 1] + (dY_A[i] / 4)
        print(f'dY[{0}] = {dY[i]}')

e = (d / 2*D) * dY
print(f'e = {e}[m]')

M_A = np.zeros(8)
for i in range(1, 8):
    if i == 1:
        M_A[i] = M[0] + M[i]
    else:
        M_A[i] = M_A[i-1] + M[i]
    
    print(f'M[{i}] = {M_A[i]}[kg]')

E = (L**3 * D * g) / ((2 * t**3) * w * d * k)
print(f'E = {E}[Pa]')