import matplotlib.pylab

R1 = 50.0
R2 = 60.0
R3 = 30.0
L2 = 5.45
i_min = 1
i_max = 2
cubic_spline_h = i_max - i_min
C2 = 0.00154
L_max = 47
L_min = 4.7
current_time = 0.0
time_step = 0.00001


def u1(time_curr):
    time_const = 0.007
    time_real = time_curr - float(time_curr // (2 * time_const)) * 2 * time_const
    if time_real > time_const:
        return 0
    else:
        return float(time_real / time_const) * 10


def l1(i1):
    if i1 <= i_min:
        return L_max
    elif i1 >= i_max:
        return L_min
    else:
        return \
            (cubic_spline_coefficients[0](i1) * L_max +
             cubic_spline_coefficients[1](i1) * L_min) / (cubic_spline_h ** 3) + \
            (cubic_spline_coefficients[2](i1) * 0 +
             cubic_spline_coefficients[3](i1) * 0) / cubic_spline_h ** 2


cubic_spline_coefficients = [
    lambda x: (2 * (x - i_min) + cubic_spline_h) * ((i_max - x) ** 2),
    lambda x: (2 * (i_max - x) + cubic_spline_h) * ((x - i_min) ** 2),
    lambda x: (x - i_min) * (i_max - x) ** 2,
    lambda x: (x - i_max) * (i_min - x) ** 2
]

differential_equations = [
    lambda t, u20, i10, i20: 1 / C2 * i20,
    lambda t, u20, i10, i20: 1 / l1(i10) * (u1(t) - i10 * (R1 + R3) + i20 * R3),
    lambda t, u20, i10, i20: 1 / L2 * (i10 * R3 - u20 - i20 * (R2 + R3))
]

# x0 - U2
# x1 - i1
# x2 - i2


def get_runge_kutta_coefficients(ARG_PREVIOUS):
    global current_time
    global time_step
    NEW_COEFFICIENTS = [[0 for _ in range(len(ARG_PREVIOUS))] for _ in range(4)]

    # K1
    for i in range(len(ARG_PREVIOUS)):
        NEW_COEFFICIENTS[0][i] = time_step * differential_equations[i](current_time,
                                                                       ARG_PREVIOUS[0],
                                                                       ARG_PREVIOUS[1],
                                                                       ARG_PREVIOUS[2])
    # K2
    for i in range(len(ARG_PREVIOUS)):
        NEW_COEFFICIENTS[1][i] = time_step * differential_equations[i](current_time + time_step / 2,
                                                                       ARG_PREVIOUS[0] + NEW_COEFFICIENTS[0][0] / 2,
                                                                       ARG_PREVIOUS[1] + NEW_COEFFICIENTS[0][1] / 2,
                                                                       ARG_PREVIOUS[2] + NEW_COEFFICIENTS[0][2] / 2)

    # K3
    for i in range(len(ARG_PREVIOUS)):
        NEW_COEFFICIENTS[2][i] = time_step * differential_equations[i](current_time + time_step / 2,
                                                                       ARG_PREVIOUS[0] + NEW_COEFFICIENTS[1][0] / 2,
                                                                       ARG_PREVIOUS[1] + NEW_COEFFICIENTS[1][1] / 2,
                                                                       ARG_PREVIOUS[2] + NEW_COEFFICIENTS[1][2] / 2)
    # K4
    for i in range(len(ARG_PREVIOUS)):
        NEW_COEFFICIENTS[3][i] = time_step * differential_equations[i](current_time + time_step,
                                                                       ARG_PREVIOUS[0] + NEW_COEFFICIENTS[2][0],
                                                                       ARG_PREVIOUS[1] + NEW_COEFFICIENTS[2][1],
                                                                       ARG_PREVIOUS[2] + NEW_COEFFICIENTS[2][2])

    return NEW_COEFFICIENTS


def runge_kutta_formula(ARG_PREVIOUS):
    global current_time

    NEW_COEFFICIENTS = get_runge_kutta_coefficients(ARG_PREVIOUS)

    NEW_ARGS = []
    for j in range(len(ARG_PREVIOUS)):
        K = []
        for i in range(len(NEW_COEFFICIENTS)):
            K.append(NEW_COEFFICIENTS[i][j])
        NEW_ARGS.append(ARG_PREVIOUS[j] + calculate_through_coefficients(K))

    current_time += time_step

    return NEW_ARGS


def calculate_through_coefficients(K):
    return 1 / 6 * (K[0] + 2 * (K[1] + K[2]) + K[3])


def build_graph(x_ax, y_ax, y_ax_name, x_ax_name='T'):
    matplotlib.pylab.plot(x_ax, y_ax)
    matplotlib.pylab.ylabel(y_ax_name)
    matplotlib.pylab.xlabel(x_ax_name)
    matplotlib.pylab.savefig("graphs/lab6_" + y_ax_name + ".png")
    matplotlib.pylab.clf()


if __name__ == '__main__':
    time = [i * time_step for i in range(500000)]
    current_values = [0, 0, 0]
    res_u2 = []
    res_i1 = []
    res_i2 = []
    for t in time:
        res_u2.append(current_values[0])
        res_i1.append(current_values[1])
        res_i2.append(current_values[2])
        current_values = runge_kutta_formula(current_values)

    build_graph([i * time_step for i in range(10000)], [u1(t) for t in [i * time_step for i in range(10000)]], "U1")
    build_graph(time, res_u2, "U2")
    build_graph(time, res_i1, "i1")
    build_graph(time, res_i2, "i2")
    build_graph([i * 0.001 for i in range(0, 3000)], [l1(i * 0.001) for i in range(0, 3000)], "L1", "i")
