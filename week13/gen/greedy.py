#!/usr/bin/env python

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

with open(args.input) as f:
    for line in f:
        l = line.split()
        if len(l) == 0:
            continue
        elif l[0] == 'MAX_RUNTIME':
            continue
        elif l[0] == 'MAX_DISTANCE':
            dist = l[1]
        elif l[0] == 'MAX_CLONE':
            clone = l[1]
        elif l[0] == 'MAX_LOAD':
            load = l[1]
        elif l[0] == 'NUM_GROUPS':
            num_groups = l[1]
        elif l[0] == 'TAPS':
            taps = np.zeros((int(l[1]), 2), dtype=int)
        elif l[0] == 'TAP':
            tap_idx = int(l[1])
            for i in range(0, 2):
                taps[tap_idx, i] = int(l[i + 2])

        elif l[0] == 'PINS':
            pins = np.zeros((int(l[1]), 3), dtype=int)
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

