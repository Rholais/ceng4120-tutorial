#!/usr/bin/env python

import math
import matplotlib.pyplot as plt
import numpy as np
import random

dies = [0,      200000,     400000,     500000,     600000,     800000,     900000,
        0,      1000000,    1100000,    1200000,    1300000,    1400000,    1500000]
n_tapss = [0,   4,          8,          12,         20,         20,         28,
           0,   22,         24,         26,         28,         30,         32]
n_grpss = [0,   10,         24,         32,         40,         41,         126,
           0,   70,         99,         128,        157,        186,        215]
n_pinss = [0,   4000,       5000,       6000,       7000,       7000,       9000,
           0,   7500,       8000,       8500,       9000,       9500,       10000]
dists = [0,     300000,     300000,     410000,     420000,     460000,     470000,
         0,     480000,     490000,     500000,     510000,     520000,     530000]
clones = [0,    0.2,        0.2,        0.2,        0.2,        0.2,        0.2,
          0,    0.2,        0.2,        0.2,        0.2,        0.2,        0.2]
loads = [0,     2000,       1200,       1000,       800,        2100,       800,
         0,     2100,       2100,       2100,       2100,       2100,       2100]


def check_dup(a, name):
    u, c = np.unique(a, return_counts=True, axis=0)
    dup = u[c > 1]
    if len(dup):
        print('duplicated {0}s: {1}'.format(name, dup))


def check_vio(taps, pins, tap_grp, dist, n_grps, clone, load, name):
    # print('check {0}'.format(name))

    is_slower = False
    d = np.sum(pins[:, 3] > dist)
    if d >= 2:
        # print('{0} distances are longer than {1}'.format(d, dist))
        is_slower = True
    elif d == 1:
        # print('one distance is longer than {0}'.format(dist))
        is_slower = True
    # else:
    #     print('max distance is {0}'.format(pins[:, 3].max()))

    is_larger = False
    c = tap_grp.sum() / n_grps - 1
    if c > clone:
        # print('clone {0} is more than {1}'.format(c, clone))
        is_larger = True

    is_heavier = False
    l = np.sum(taps[:, 2] > load)
    if l >= 2:
        # print('{0} loads are heavier than {1}'.format(l, load))
        is_heavier = True
    elif l == 1:
        # print('one load is heavier than {0}'.format(load))
        is_heavier = True

    return is_slower, is_larger, is_heavier


for i in [5, 8, 9, 10, 11, 12, 13]:
    die = dies[i]
    n_taps = n_tapss[i]
    taps = np.zeros((n_taps, 3), dtype=np.int64)
    for j in range(0, n_taps):
        for k in range(0, 2):
            taps[j, k] = random.randrange(die / 8, die * 7 / 8)

    check_dup(taps, 'tap')

    n_pins = n_pinss[i]
    n_grps = n_grpss[i]
    grps = np.zeros((n_grps, 6), dtype=np.int64)
    for j in range(0, n_grps):
        for k in range(0, 2):
            grps[j, k] = random.randrange(die / 4)

    pins = np.zeros((n_pins, 5), dtype=np.int64)
    for j in range(0, n_pins):
        g = random.randrange(n_grps)
        pins[j, 2] = g
        for k in range(0, 2):
            pins[j, k] = grps[g, k] + random.randrange(die * 3 / 4)

    check_dup(pins[:, 0:2], 'pin')

    dist = dists[i]
    clone = clones[i]
    load = loads[i]
    tap_grp = np.zeros((n_taps, n_grps), dtype=int)
    while True:
        print('dist {0}\t clone {1}\tload {2}'.format(dist, clone, load))
        taps[:, 2] = 0
        tap_grp = np.zeros((n_taps, n_grps), dtype=int)
        for j in range(0, n_pins):
            d = np.absolute(taps[:, 0:2] - pins[j, 0:2]).sum(axis=1)
            pins[j, 3] = d.min()
            t = d.argmin()
            pins[j, 4] = t
            taps[t, 2] += 1
            g = pins[j, 2]
            tap_grp[t, g] = 1

        is_slower, is_larger, is_heavier = check_vio(
            taps, pins, tap_grp, dist, n_grps, clone, load, 'dist')
        if not (is_slower or is_larger or is_heavier):
            break

        grps[:, 2:5] = np.zeros((n_grps, 3), dtype=np.int64)
        for j in range(0, n_pins):
            g = pins[j, 2]
            grps[g, 2:4] += pins[j, 0:2]
            grps[g, 4] += 1

        if not grps[:, 4].min():
            print('group {0} is empty'.format(grps[:, 2].argmin()))

        centers = np.zeros((n_grps, 2))
        for j in range(0, 2):
            centers[:, j] = grps[:, j + 2] / grps[:, 4]

        taps[:, 2] = 0
        for j in range(0, n_grps):
            t = np.absolute(taps[:, 0:2] - centers[j, 0:2]
                            ).sum(axis=1).argmin()
            grps[j, 5] = t
            taps[t, 2] += grps[j, 4]

        tap_grp = np.zeros((n_taps, n_grps), dtype=int)
        for j in range(0, n_pins):
            g = pins[j, 2]
            t = grps[g, 5]
            pins[j, 3] = np.absolute(taps[t, 0:2] - pins[j, 0:2]).sum()
            pins[j, 4] = t
            tap_grp[t, g] = 1

        s, l, h = check_vio(taps, pins, tap_grp, dist,
                            n_grps, clone, load, 'group')
        if not (s or l or h):
            break

        is_slower = is_slower or s
        is_larger = is_larger or s
        is_heavier = is_heavier or h

        if is_slower:
            dist *= 1.01

        if is_larger:
            clone *= 1.00

        if is_heavier:
            load *= 1.01

        c = pins[:, 0:2].mean(axis=0, dtype=float)
        cgm = math.sqrt(np.power(centers - c, 2).sum(axis=1).max())
        for j in range(0, n_pins):
            g = pins[j, 2]
            cg = centers[g]
            cga = abs(cg - c) / cgm
            pins[j, 0:2] = (pins[j, 0:2] - c) * 0.984 + (cg - c) * 0.008 + \
                (random.randrange(die) - c) * 0.001
            for k in range(0, 2):
                if cg[k] > c[k]:
                    pins[j, k] += (die * cga[k] * 0.004)
                elif cg[k] < c[k]:
                    pins[j, k] -= (die * cga[k] * 0.004)

                pins[j, k] += c[k]

    print(np.sum(tap_grp.sum(axis=1) > 0))
    plt.scatter(pins[:, 0], pins[:, 1], c=pins[:, 2], alpha=0.5)
    plt.show()

    f = open('test{0}.in'.format(i), 'w')
    f.write('MAX_RUNTIME 3600\n')
    f.write('MAX_DISTANCE {0}\n'.format(dist / 1.02))
    f.write('MAX_CLONE {0}\n'.format(clone / 1.00))
    f.write('MAX_LOAD {0}\n'.format(load / 1.02))
    f.write('NUM_GROUPS {0}\n\n'.format(n_grps))

    f.write('TAPS {0}\n'.format(n_taps))
    for j in range(0, n_taps):
        f.write('    TAP {0} {1} {2}\n'.format(j, taps[j, 0], taps[j, 1]))

    f.write('END TAPS\n\n')

    f.write('PINS {0}\n'.format(n_pins))
    for j in range(0, n_pins):
        f.write('    PIN {0} {1} {2} {3}\n'.format(
            j, pins[j, 0], pins[j, 1], pins[j, 2]))

    f.write('END PINS\n\n')
