#!/usr/bin/env python

with open('mlp.vh', 'w') as f:
    num_layers = 2
    for i in range(0, 2):
        for j in range(0, num_layers + 2):
            if i:
                f.write('module nrs{0}(y, a0, a1, a2, a3, a4);\n'.format(j))
            else:
                f.write('module nrn{0}(y, a0, a1, a2, a3, a4);\n'.format(j))

            f.write('    output [7:0] y;\n')
            for k in range(0, 5):
                f.write('    input [7:0] a{0};\n'.format(k))

            f.write('\n')
            if i:
                f.write('    NEUROS{0} n(\n'.format(j))
            else:
                f.write('    NEURON{0} n(\n'.format(j))

            for k in range(0, 8):
                f.write('        .Y{0}(y[{0}]),\n'.format(k))
                for l in range(0, 5):
                    if k == 7 and l == 4:
                        f.write('        .A47(a4[7]));\n')
                    else:
                        f.write('        .A{0}{1}(a{0}[{1}]),\n'.format(l, k))

            f.write('endmodule\n\n')

    f.write('module mlp(y, a);\n')
    f.write('    output [79:0] y;\n')
    f.write('    input [{0}:0] a;\n\n'.format(num_layers * 32 + 143))

    for i in range(0, num_layers + 1):
        for j in range(0, i * 4 + 14):
            f.write('    wire [7:0] n{0}{1};\n'.format(i + 1, j))

    f.write('\n')
    for i in range(0, 10):
        if i % 2:
            f.write('    nrs0 nrs0{0}(\n'.format(i))
        else:
            f.write('    nrn0 nrn0{0}(\n'.format(i))

        f.write('        .y(y[{0}:{1}]),\n'.format(i * 8 + 7, i * 8))
        for j in range(0, 4):
            f.write('        .a{0}(n1{1}),\n'.format(j, i + j))

        f.write('        .a4(n1{0}));\n'.format(i + 4))

    for i in range(0, num_layers):
        for j in range(0, i * 4 + 14):
            if (j >= i - 1 and j < i * 3 + 15 and j % 2) or (i % 2 == 0 and j < i - 1) or (i % 2 and j >= i * 3 + 15):
                f.write('    nrs{0} nrs{0}{1}(\n'.format(i + 1, j))
            else:
                f.write('    nrn{0} nrn{0}{1}(\n'.format(i + 1, j))

            f.write('        .y(n{0}{1}),\n'.format(i + 1, j))
            for k in range(0, 4):
                f.write('        .a{0}(n{1}{2}),\n'.format(k, i + 2, j + k))

            f.write('        .a4(n{0}{1}));\n'.format(i + 2, j + 4))

    for i in range(0, num_layers * 4 + 14):
        if (i >= num_layers - 1 and i < num_layers * 3 + 15 and i % 2) or (num_layers % 2 == 0 and i < num_layers - 1) or (num_layers % 2 and i >= num_layers * 3 + 15):
            f.write('    nrs{0} nrs{0}{1}(\n'.format(num_layers + 1, i))
        else:
            f.write('    nrn{0} nrn{0}{1}(\n'.format(num_layers + 1, i))

        f.write('        .y(n{0}{1}),\n'.format(num_layers + 1, i))
        for j in range(0, 4):
            f.write('        .a{0}(a[{1}:{2}]),\n'.format(j, i * 8 + j * 8 + 7, i * 8 + j * 8))

        f.write('        .a4(a[{0}:{1}]));\n'.format(i * 8 + 39, i * 8 + 32))

    f.write('endmodule\n\n')
