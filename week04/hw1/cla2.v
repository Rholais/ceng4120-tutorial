
//  2-Bit Carry Look Ahead Adder

module cla2 (sum, c2, a, b, c0);

    output  [1:0]   sum;
    output          c2;
    input   [1:0]   a;
    input   [1:0]   b;
    input           c0;

    wire            c1;
    wire    [1:0]   g;
    wire    [1:0]   p;

    wire            and100_out;
    wire            and110_out;
    wire            and111_out;

    and and00(g[0], a[0], b[0]);
    and and01(g[1], a[1], b[1]);

    or or00(p[0], a[0], b[0]);
    or or01(p[1], a[1], b[1]);

    and and100(and100_out, p[0], c0);

    and and110(and110_out, p[1], p[0], c0);
    and and111(and111_out, p[1], g[0]);

    or  or20(c1, g[0], and100_out);
    or  or21(c2, g[1], and110_out, and111_out);

    xor xor30(sum[0], a[0], b[0], c0);
    xor xor31(sum[1], a[1], b[1], c1);

endmodule

