#/**************************************************/
#/* Compile Script for Synopsys                    */
#/*                                                */
#/* dc_shell-t -f compile_dc.tcl                   */
#/*                                                */
#/* OSU FreePDK 45nm                               */
#/**************************************************/

#/* All verilog files, separated by spaces         */
set my_verilog_file "cla2.v"

#/* Top-level Module                               */
set my_toplevel cla2

#/**************************************************/
#/* No modifications needed below                  */
#/**************************************************/
set target_library "gscl45nm.db"
set link_library "gscl45nm.db"

analyze -f verilog $my_verilog_file
elaborate $my_toplevel

compile_ultra

set filename [format "%s%s"  $my_toplevel ".vh"]
write_file -f verilog -output $filename

redirect timing.rep { report_timing }
redirect cell.rep { report_cell }
redirect power.rep { report_power }

quit

