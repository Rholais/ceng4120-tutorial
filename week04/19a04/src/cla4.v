
//  4-Bit Carry Look Ahead Adder

module cla4 (sum, cout, a, b, cin);

    output  [3:0]   sum;
    output          cout;
    input   [3:0]   a;
    input   [3:0]   b;
    input           cin;

    wire    [2:0]   c;
    wire    [3:0]   g;
    wire    [3:0]   p;

    wire            and100_out;
    wire            and110_out;
    wire            and111_out;
    wire            and120_out;
    wire            and121_out;
    wire            and122_out;
    wire            and130_out;
    wire            and131_out;
    wire            and132_out;
    wire            and133_out;

    and and00(g[0], a[0], b[0]);
    and and01(g[1], a[1], b[1]);
    and and02(g[2], a[2], b[2]);
    and and03(g[3], a[3], b[3]);

    or or00(p[0], a[0], b[0]);
    or or01(p[1], a[1], b[1]);
    or or02(p[2], a[2], b[2]);
    or or03(p[3], a[3], b[3]);

    and and100(and100_out, p[0], cin);

    and and110(and110_out, p[1], p[0], cin);
    and and111(and111_out, p[1], g[0]);

    and and120(and120_out, p[2], p[1], p[0], cin);
    and and121(and121_out, p[2], p[1], g[0]);
    and and122(and122_out, p[2], g[1]);

    and and130(and130_out, p[3], p[2], p[1], p[0], cin);
    and and131(and131_out, p[3], p[2], p[1], g[0]);
    and and132(and132_out, p[3], p[2], g[1]);
    and and133(and133_out, p[3], g[2]);

    or  or20(c[0], g[0], and100_out);
    or  or21(c[1], g[1], and110_out, and111_out);
    or  or22(c[2], g[2], and120_out, and121_out, and122_out);
    or  or23(cout, g[3], and130_out, and131_out, and132_out, and133_out);

    xor xor30(sum[0], a[0], b[0], cin);
    xor xor31(sum[1], a[1], b[1], c[0]);
    xor xor32(sum[2], a[2], b[2], c[1]);
    xor xor33(sum[3], a[3], b[3], c[2]);

endmodule

