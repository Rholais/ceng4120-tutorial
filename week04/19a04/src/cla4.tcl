#/**************************************************/
#/* Compile Script for Synopsys                    */
#/*                                                */
#/* dc_shell-t -f compile_dc.tcl                   */
#/*                                                */
#/* OSU FreePDK 45nm                               */
#/**************************************************/

#/* Top-level Module                               */
set top cla4

#/**************************************************/
#/* No modifications needed below                  */
#/**************************************************/
set target_library "gscl45nm.db"
set link_library "gscl45nm.db"

analyze -f verilog ${top}.v
elaborate ${top}

compile_ultra

set filename [format "%s%s"  ${top} ".vh"]
write_file -f verilog -output $filename

redirect timing.rep { report_timing }
redirect cell.rep { report_cell }
redirect power.rep { report_power }

set_max_delay -from {a*} -to {s*} 0.28

compile_ultra

set filename [format "%s%s"  ${top} "-fast.vh"]
write_file -f verilog -output $filename

redirect "timing-fast.rep" { report_timing }
redirect "cell-fast.rep" { report_cell }
redirect "power-fast.rep" { report_power }

quit
