#!/usr/bin/env python

with open('net.vh', 'w') as f:
    num_col = 9
    num_row = 12
    f.write('module net(y, a);\n')
    f.write('    output [{0}:0] y;\n'.format(num_row - 1))
    f.write('    input [{0}:0] a;\n\n'.format(num_col * 4 + num_row - 1))

    for i in range(1, num_col):
        for j in range(0, num_row):
            f.write('    wire n{0}{1};\n'.format(i, j))

    f.write('\n')
    for i in range(0, num_row):
        if i % 2:
            f.write('    NEURON0 nrn0{0}(\n'.format(i))
        else:
            f.write('    NEUROS0 nrs0{0}(\n'.format(i))

        f.write('        .Y0(y[{0}]),\n'.format(i))
        if i == 0:
            for j in range(0, 2):
                f.write('        .A{0}0(a[{0}]),\n'.format(j))

            for j in range(0, 2):
                f.write('        .A{0}0(n1{1}),\n'.format(j + 2, j))

            f.write('        .A40(y[1]));\n')
        elif i == num_row - 1:
            f.write('        .A00(y[{0}]),\n'.format(num_row - 2))
            for j in range(0, 2):
                f.write('        .A{0}0(n1{1}),\n'.format(j + 1, num_row + j - 2))

            f.write('        .A30(a[{0}]),\n'.format(num_col * 4 + num_row - 2))
            f.write('        .A40(a[{0}]));\n'.format(num_col * 4 + num_row - 1))

        else:
            f.write('        .A00(y[{0}]),\n'.format(i - 1))
            for j in range(0, 3):
                f.write('        .A{0}0(n1{1}),\n'.format(j + 1, i + j - 1))

            f.write('        .A40(y[{0}]));\n'.format(i + 1))

    for i in range(0, num_col - 2):
        for j in range(0, num_row):
            if j % 2:
                f.write('    NEURON0 nrn{0}{1}(\n'.format(i + 1, j))
            else:
                f.write('    NEUROS0 nrs{0}{1}(\n'.format(i + 1, j))

            f.write('        .Y0(n{0}{1}),\n'.format(i + 1, j))
            if j == 0:
                for k in range(0, 2):
                    f.write('        .A{0}0(a[{1}]),\n'.format(k, i * 2 + k + 2))

                for k in range(0, 2):
                    f.write('        .A{0}0(n{1}{2}),\n'.format(k + 2, i + 2, i + k))

                f.write('        .A40(n{0}{1}));\n'.format(i + 1, 1))
            elif j == num_row - 1:
                f.write('        .A00(n{0}{1}),\n'.format(i + 1, num_row - 2))
                for k in range(0, 2):
                    f.write('        .A{0}0(n{1}{2}),\n'.format(k + 1, i + 2, num_row + k - 2))

                f.write('        .A30(a[{0}]),\n'.format(-i * 2 + num_col * 4 + num_row - 4))
                f.write('        .A40(a[{0}]));\n'.format(-i * 2 + num_col * 4 + num_row - 3))

            else:
                f.write('        .A00(n{0}{1}),\n'.format(i + 1, j - 1))
                for k in range(0, 3):
                    f.write('        .A{0}0(n{1}{2}),\n'.format(k + 1, i + 2, j + k - 1))

                f.write('        .A40(n{0}{1}));\n'.format(i + 1, j + 1))

    for i in range(0, num_row):
        if i % 2:
            f.write('    NEURON0 nrn{0}{1}(\n'.format(num_col - 1, i))
        else:
            f.write('    NEUROS0 nrs{0}{1}(\n'.format(num_col - 1, i))

        f.write('        .Y0(n{0}{1}),\n'.format(num_col - 1, i))
        for j in range(0, 4):
            f.write('        .A{0}0(a[{1}]),\n'.format(j, i + j + num_col * 2 - 2))

        f.write('        .A40(a[{0}]));\n'.format(i + num_col * 2 + 2))

    f.write('endmodule\n\n')

