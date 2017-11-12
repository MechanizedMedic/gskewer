# gskewer
A tool to skew transform gcode coordinates to account for axis misalignment.

The task of measuring the error between axis pairs is shown in good detail at https://reprappro.com/documentation/ormerod/axis-compensation/#Setting_the_compensation_from_the_printed_test_parts

The G-code file to be modified, the measured error (in mm), and the distance from zero where the measurement was taken is then entered into skew.py before being run.