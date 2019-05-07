#!/bin/tcsh

setenv SYNOPSYS /opt2/synopsys
setenv SNPSLMD_LICENSE_FILE $SYNOPSYS/key
setenv LM_LICENSE_FILE $SYNOPSYS/key

set path=($path $SYNOPSYS/syn-J-2014.09-SP5-6/bin)
