set top mlp

set init_verilog ${top}.vh
set init_top_cell ${top}
set init_design_netlisttype Verilog
set init_design_settop 1
set init_design_uniquify 1
set init_io_file {}
set init_lef_file ${top}.lef
# set init_pwr_net vdd
# set init_gnd_net gnd
init_design

# Create Initial Floorplan
floorplan -r 1.0 0.79 1.2 1.2 1.2 1.2

# Create Power structures
# addRing -spacing_bottom 5 -width_left 5 -width_bottom 5 -width_top 5 -spacing_top 5 -layer_bottom metal5 -width_right 5 -around core -center 1 -layer_top metal5 -             spacing_right 5 -spacing_left 5 -layer_right metal6 -layer_left metal6 -nets { gnd vdd }
# addRing -spacing 5 -width 5 -layer {top metal3 bottom metal3 left metal4 right metal4} -center 1 -nets { gnd vdd }

specifyScanChain ${top}_sc -start a[0] -stop y[0]
setScanReorderMode -compLogic true
# setNanoRouteMode -routeUseAutoVia true

# Place standard cells
# setPlaceMode -place_global_clock_gate_aware false
defIn ${top}.py.def
place_design
defOut ${top}.def

# Route power nets
# sroute

# Add filler cells
# addFiller -cell FILL -prefix FILL -fillBoundary

# Connect all new cells to VDD/GND
# globalNetConnect vdd -type tiehi
# globalNetConnect vdd -type pgpin -pin vdd -override

# globalNetConnect gnd -type tielo
# globalNetConnect gnd -type pgpin -pin gnd -override

# Run global Routing
# globalDetailRoute
setDesignMode -process 32
routeDesign

# Get final timing results
# setExtractRCMode -detail -noReduce
setExtractRCMode -engine postRoute
extractRC
# buildTimingGraph
setCteReport

# Run DRC and Connection checks
verify_drc
verifyConnectivity -type all

highlight " [ dbGet top.insts.name nr?0* ] " -index 1
highlight " [ dbGet top.insts.name nr?1* ] " -index 2
highlight " [ dbGet top.insts.name nr?2* ] " -index 3
highlight " [ dbGet top.insts.name nr?3* ] " -index 15

win

puts "**************************************"
puts "* Encounter script finished          *"
puts "*                                    *"
puts "* Results:                           *"
puts "* --------                           *"
puts "* Layout:  final.gds2                *"
puts "* Netlist: final.v                   *"
puts "* Timing:  timing.rep.5.final        *"
puts "*                                    *"
puts "* Type 'exit' to quit                *"
puts "*                                    *"
puts "**************************************"

