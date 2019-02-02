# gskewer
A tool to skew transform gcode coordinates to account for axis misalignment.

The task of measuring the error between axis pairs is shown in good detail at http://www.zs1jen.org/Station_Manuals/Reference/3D_Printers/14_RepRapPro_-_Axis_compensation.pdf

The G-code file to be modified, the measured error (in mm), and the distance from zero where the measurement was taken is then entered into skew.py before being run.
