#!/usr/bin/env python3

BEGIN = '''
VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN net ;
UNITS DISTANCE MICRONS 2000 ;

PROPERTYDEFINITIONS
    COMPONENTPIN designRuleWidth REAL ;
    DESIGN FE_CORE_BOX_LL_X REAL 1.200 ;
    DESIGN FE_CORE_BOX_UR_X REAL 15.800 ;
    DESIGN FE_CORE_BOX_LL_Y REAL 1.200 ;
    DESIGN FE_CORE_BOX_UR_Y REAL 15.600 ;
END PROPERTYDEFINITIONS

DIEAREA ( 0 0 ) ( 34000 33600 ) ;

ROW CORE_ROW_0 CoreSite 2400 2400 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_1 CoreSite 2400 4800 N DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_2 CoreSite 2400 7200 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_3 CoreSite 2400 9600 N DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_4 CoreSite 2400 12000 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_5 CoreSite 2400 14400 N DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_6 CoreSite 2400 16800 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_7 CoreSite 2400 19200 N DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_8 CoreSite 2400 21600 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_9 CoreSite 2400 24000 N DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_10 CoreSite 2400 26400 FS DO 146 BY 1 STEP 200 0
 ;
ROW CORE_ROW_11 CoreSite 2400 28800 N DO 146 BY 1 STEP 200 0
 ;

TRACKS Y 500 DO 83 STEP 400 LAYER Metal9 ;
TRACKS X 500 DO 84 STEP 400 LAYER Metal9 ;
TRACKS X 500 DO 84 STEP 400 LAYER Metal8 ;
TRACKS Y 500 DO 83 STEP 400 LAYER Metal8 ;
TRACKS Y 400 DO 111 STEP 300 LAYER Metal7 ;
TRACKS X 400 DO 112 STEP 300 LAYER Metal7 ;
TRACKS X 400 DO 112 STEP 300 LAYER Metal6 ;
TRACKS Y 400 DO 111 STEP 300 LAYER Metal6 ;
TRACKS Y 100 DO 168 STEP 200 LAYER Metal5 ;
TRACKS X 100 DO 170 STEP 200 LAYER Metal5 ;
TRACKS X 100 DO 170 STEP 200 LAYER Metal4 ;
TRACKS Y 100 DO 168 STEP 200 LAYER Metal4 ;
TRACKS Y 100 DO 168 STEP 200 LAYER Metal3 ;
TRACKS X 100 DO 170 STEP 200 LAYER Metal3 ;
TRACKS X 100 DO 170 STEP 200 LAYER Metal2 ;
TRACKS Y 100 DO 168 STEP 200 LAYER Metal2 ;
TRACKS Y 100 DO 168 STEP 200 LAYER Metal1 ;
TRACKS X 100 DO 170 STEP 200 LAYER Metal1 ;

GCELLGRID X 32100 DO 2 STEP 1900 ;
GCELLGRID X 100 DO 17 STEP 2000 ;
GCELLGRID X 0 DO 2 STEP 100 ;
GCELLGRID Y 32100 DO 2 STEP 1500 ;
GCELLGRID Y 100 DO 17 STEP 2000 ;
GCELLGRID Y 0 DO 2 STEP 100 ;

COMPONENTS 108 ;
'''

END = '''
END PINS

END DESIGN

'''

with open('net.py.def', 'w') as f:
    f.write(BEGIN);
    num_col = 9
    num_row = 12
    for i in range(0, num_col):
        for j in range(0, num_row):
            x = (num_col - i - 1) * 3200 + 2600
            y = (j + 1) * 2400

            if y % 4800:
                f.write('- nrs{0}{1} NEUROS0 + PLACED ( {2} {3} ) FS\n'.format(i, j, x, y))
            else:
                f.write('- nrn{0}{1} NEURON0 + PLACED ( {2} {3} ) N\n'.format(i, j, x, y))

            f.write(' ;\n')

    f.write('END COMPONENTS\n\n')
    f.write('PINS {0} ;\n'.format(num_row * 2 + num_col * 4))
    for i in range(0, num_row):
        f.write('- y[{0}] + NET y[{0}] + DIRECTION OUTPUT + USE SIGNAL\n'.format(i))
        f.write('  + LAYER Metal2 ( -50 0 ) ( 50 560 )\n')
        f.write('  + PLACED ( 34000 {0} ) W ;\n'.format((i + 1) * 2400 + 1200))

    for i in range(0, num_row + num_col * 4):
        f.write('- a[{0}] + NET a[{0}] + DIRECTION INPUT + USE SIGNAL\n'.format(i))
        if i < num_col * 2:
            f.write('  + LAYER Metal3 ( -50 0 ) ( 50 680 )\n')
            f.write('  + PLACED ( {0} 0 ) N ;\n'.format((num_col - i // 2 - 1) * 3200 - (i % 2) * 200 + 3300))
        elif i >= num_row + num_col * 2:
            f.write('  + LAYER Metal3 ( -50 0 ) ( 50 680 )\n')
            idx = i - num_row - num_col * 2
            f.write('  + PLACED ( {0} 33600 ) S ;\n'.format((idx // 2) * 3200 + (idx % 2) * 200 + 3100))
        else:
            f.write('  + LAYER Metal2 ( -50 0 ) ( 50 560 )\n')
            f.write('  + PLACED ( 0 {0} ) E ;\n'.format((i - num_col * 2 + 1) * 2400 + 1200))

    f.write(END);

