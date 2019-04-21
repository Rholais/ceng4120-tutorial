#!/usr/bin/env python

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

with open(args.input) as f:
    for line in f:
        l = line.split()
        if len(l) == 0:
            continue
        elif l[0] == 'MAX_RUNTIME':
            continue
        elif l[0] == 'MAX_DISTANCE':
            dist = int(l[1])
        elif l[0] == 'MAX_CLONE':
            clone = float(l[1])
        elif l[0] == 'MAX_LOAD':
            load = int(l[1])
        elif l[0] == 'NUM_GROUPS':
            num_groups = int(l[1])
        elif l[0] == 'TAPS':
            num_taps = int(l[1])
            taps = np.zeros((num_taps, 2), dtype=int)
        elif l[0] == 'TAP':
            tap_idx = int(l[1])
            for i in range(0, 2):
                taps[tap_idx, i] = int(l[i + 2])

        elif l[0] == 'PINS':
            num_pins = int(l[1])
            pins = np.zeros((num_pins, 4), dtype=int)
        elif l[0] == 'PIN':
            pin_idx = int(l[1])
            for i in range(0, 3):
                pins[pin_idx, i] = int(l[i + 2])

        elif l[0] == 'END' and l[1] == 'TAPS':
            # print(taps)
            continue
        elif l[0] == 'END' and l[1] == 'PINS':
            # print(pins)
            continue
        else:
            print(l)

with open(args.output) as f:
    for line in f:
        l = line.split()
        if len(l) == 0:
            continue
        else:
            pins[int(l[0]), 3] = int(l[1])

d = 0
g = 0
l = 0
h = 0
for i in range(0, num_taps):
    idx = pins[:, 3] == i
    if idx.sum() == 0:
        continue
    else:
        pin = pins[idx]

    d = max(d, np.absolute(pin[:, 0:2] - taps[i]).sum(axis=1).max())
    g += np.unique(pin[:, 2]).shape[0]
    l = max(l, pin.shape[0])
    h += np.sum(pin[0:2].max(axis=0) - pin[0:2].min(axis=0))

c = g / num_groups - 1
print('max dist : {0}'.format(d))
print('clone    : {0}'.format(c))
print('max load : {0}'.format(l))
print('hpwl     : {0}'.format(h))
if d > dist:
    print('score    : max dist exceeds {0}'.format(dist))
elif l > load:
    print('score    : max load exceeds {0}'.format(load))
else:
    print('score    : {0}'.format(h * (1 + 5 * max(c - clone, 0))))

