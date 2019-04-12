#!/bin/env python

import numpy as np
import random

dies    = [ 200000, 400000, 500000, 600000, 800000, 900000, 1000000 ]
n_tapss = [ 4,      8,      12,     20,     24,     28,     32      ]
n_lvss  = [ 1,      2,      2,      2,      3,      3,      3       ]
n_ch1ss = [ 10,     6,      8,      8,      5,      6,      7       ]
n_ch2ss = [ 10,     3,      3,      4,      3,      4,      5       ]
n_ch3ss = [ 10,     3,      3,      4,      3,      4,      5       ]
n_pinss = [ 4000,   5000,   6000,   7000,   8000,   9000,   10000   ]
dists   = [ 300000, 420000, 430000, 450000, 480000, 510000, 530000  ]
clone   = [ 0.2,    0.2,    0.2,    0.2,    0.2,    0.2,    0.2     ]
loads   = [ 2000,   1200,   1000,   800,    600,    600,    600     ]


def check_dup(a, name):
    u, c = np.unique(a, return_counts=True, axis=0)
    dup = u[c > 1]
    if len(dup):
        print('duplicated {0}s: {1}'.format(name, dup))


def check_vio(taps, pins, tap_group, dist, n_groups, clone, load, name):
    print('check {0}'.format(name))

    is_slower = False
    d = np.sum(pins[:, 3] > dist);
    if d >= 2:
        print('{0} distances are longer than {1}'.format(d, dist))
        is_slower = True
    elif d == 1:
        print('one distance is longer than {0}'.format(dist))
        is_slower = True
    # else:
    #     print('max distance is {0}'.format(pins[:, 3].max()))

    is_larger = False
    c = tap_group.sum() / n_groups - 1
    if c > clone:
        print('clone {0} is more than {1}'.format(c, clone))
        is_larger = True

    is_heavier = False
    l = np.sum(taps[:, 2] > load)
    if l >= 2:
        print('{0} loads are heavier than {1}'.format(l, load))
        is_heavier = True
    elif l == 1:
        print('one load is heavier than {0}'.format(load))
        is_heavier = True

    return is_slower, is_larger, is_heavier


for i in range(0, 7):
    die = dies[i]
    n_taps = n_tapss[i]
    taps = np.zeros((n_taps, 3), dtype=np.int64)
    for j in range(0, n_taps):
        for k in range(0, 2):
            taps[j, k] = random.randrange(die / 8, die * 7 / 8)

    check_dup(taps, 'tap')

    n_pins = n_pinss[i]
    n_ch1s = n_ch1ss[i]
    n_ch2s = n_ch2ss[i]
    n_ch3s = n_ch3ss[i]
    n_groups = n_ch1s
    n_lvs = n_lvss[i]
    if n_lvs == 3:
        n_groups += n_ch1s * n_ch2s + n_ch1s * n_ch2s * n_ch3s
    elif n_lvs == 2:
        n_groups += n_ch1s * n_ch2s

    pins = np.zeros((n_pins, 5), dtype=np.int64)
    for j in range(0, n_pins):
        pins[j, 2] = random.randrange(n_groups)
        for k in range(0, 2):
            pins[j, k] = random.randrange(die)

    check_dup(pins[:, 0:2], 'pin')

    dist = dists[i]
    load = loads[i]
    while True:
        taps[:, 2] = 0
        tap_group = np.zeros((n_taps, n_groups), dtype=int)
        for j in range(0, n_pins):
            d = np.absolute(taps[:, 0:2] - pins[j, 0:2]).sum(axis=1)
            pins[j, 3] = d.min()
            t = d.argmin()
            pins[j, 4] = t
            taps[t, 2] += 1
            g = pins[j, 2]
            tap_group[t, g] = 1
            if n_lvs == 3 and g >= n_ch1s * (1 + n_ch2s):
                ppg = ((g - n_ch1s) // n_ch2s - n_ch1s) // n_ch3s
                tap_group[t, ppg] = 1
                tap_group[t, (g - n_ch1s * (1 + n_ch2s)) // n_ch3s - n_ch2s * ppg] = 1
            elif n_lvs >= 2 and g >= n_ch1s:
                tap_group[t, (g - n_ch1s) // n_ch2s] = 1

        is_slower, is_larger, is_heavier = check_vio(taps, pins, tap_group, dist, n_groups, clone[i], load, 'dist')
        if not (is_slower or is_larger or is_heavier):
            print(tap_group)
            break

        groups = np.zeros((n_groups, 4), dtype=np.int64)
        for j in range(0, n_pins):
            g = pins[j, 2]
            groups[g, 0:2] += pins[j, 0:2]
            groups[g, 2] += 1

        if not groups[:, 2].min():
            print('group {0} is empty'.format(groups[:, 2].argmin()))

        centers = np.zeros((n_groups, 2))
        for j in range(0, 2):
            centers[:, j] = groups[:, j] / groups[:, 2]

        taps[:, 2] = 0
        for j in range(0, n_groups):
            t = np.absolute(taps[:, 0:2] - centers[j, 0:2]).sum(axis=1).argmin()
            groups[j, 3] = t
            taps[t, 2] += groups[j, 2]

        tap_group = np.zeros((n_taps, n_groups), dtype=int)
        for j in range(0, n_pins):
            g = pins[j, 2]
            t = groups[g, 3]
            pins[j, 3] = np.absolute(taps[t, 0:2] - pins[j, 0:2]).sum()
            pins[j, 4] = t
            tap_group[t, g] = 1
            if n_lvs == 3 and g >= n_ch1s * (1 + n_ch2s):
                ppg = ((g - n_ch1s) // n_ch2s - n_ch1s) // n_ch3s
                tap_group[t, ppg] = 1
                tap_group[t, (g - n_ch1s * (1 + n_ch2s)) // n_ch3s - n_ch2s * ppg] = 1
            elif n_lvs >= 2 and g >= n_ch1s:
                tap_group[t, (g - n_ch1s) // n_ch2s] = 1

        s, l, h = check_vio(taps, pins, tap_group, dist, n_groups, clone[i], load, 'group')
        if not (s or l or h):
            print(tap_group)
            break

        is_slower = is_slower or s
        is_larger = is_larger or s
        is_heavier = is_heavier or h

        if is_slower:
            dist *= 1.1

        if is_heavier:
            load *= 1.01

        c = pins[:, 0:2].mean(axis=0, dtype=float)
        for j in range(0, n_pins):
            for k in range(0, 2):
                g = pins[j, 2]
                pg = pins[j, 2]
                ppg = pins[j, 2]
                if n_lvs == 3 and g >= n_ch1s * (1 + n_ch2s):
                    ppg = ((g - n_ch1s) // n_ch2s - n_ch1s) // n_ch3s
                    pg = (g - n_ch1s * (1 + n_ch2s)) // n_ch3s - n_ch2s * ppg
                elif n_lvs >= 2 and g >= n_ch1s:
                    pg = (g - n_ch1s) // n_ch2s

                cg = centers[g, k]
                cpg = centers[pg, k]
                cppg = centers[ppg, k]
                pins[j, k] = pins[j, k] * 0.90 + cg * 0.01 + cpg * 0.04 + cppg * 0.01 # + random.randrange(die) * 0.001
                if cg > c[k]:
                    pins[j, k] += (die - 1) * 0.04
                elif cg == c[k]:
                    pins[j, k] += c[k] * 0.04

    # print(pins)

