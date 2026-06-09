# About Gskewer
Gskewer is a tool to skew transform gcode file coordinates to account for axis misalignment of a 3D printer.

In order to use Gskewer you will need to print a test cube, take accurate measurements of the cube, then input those measurements as arguments for Gskewer. You can also use Calilantern or Califlower, and use the SKEW_FACTORs generated for Marlin or RepRap firmwares.

The G-code file to be modified, the measured error (in mm), and the distance from zero where the measurement was taken is then entered into skew.py before being run.

This can be added as a slicer post-processing script.


# Preparing to use Gskewer
The task of measuring the error between axis pairs is shown in good detail at http://www.zs1jen.org/Station_Manuals/Reference/3D_Printers/14_RepRapPro_-_Axis_compensation.pdf

The files to be printed for the above process are at https://github.com/reprappro/RepRapFirmware/blob/master/STL/calibration_90mm.stl

The general idea of the measurements required and which arguments they correspond to is illustrated below.

![MechanizedMedic](https://github.com/MechanizedMedic/gskewer/raw/master/gskewer_measuring1.png "Positive skew error.")
![MechanizedMedic](https://github.com/MechanizedMedic/gskewer/raw/master/gskewer_measuring2.png "Negative skew error.")

These measurements are to be taken for each of the three axis pairs of the cube: XY, YZ, and xz.

You will end up with six measurements/arguments: xylen, xyerr, yzlen, yzerr, xzlen, and xzerr.

The initial six measurements can be simplified to a skew argument by dividing the error by length (ie: xyerr/xylen=xyskew). The skew arguments are: xyskew, yzskew, and xzskew.


# Using Gskewer
`gskewer [arguements] file`

Gskewer will automatically generate a new gcode file with "-skewed" added to the file name. If the output file name already exists gskewer will delete the existing file and write a new one.

### Examples

`gskewer --xyerr 1.2 --xylen 80 --yzskew 0 --xzskew 0 Cube80mm.gcode` will adjust the X coordinate proportionally by -1.2 mm for every 80mm in the Y coordinate. The output file will be "Cube80mm-skewed.gcode".

`--xyskew 0.015` is equivalent in the example above, as `xyskew = xyerr / xylen`. The skew factors are 

### Gskewer Arguments
`--xyerr`
	Error in the X-axis for the XY pair in mm. (This argument cannot be used with "xyskew")

`--xylen`
	Length of the test cube side where the "xyerr" measurement was taken.

`--xyskew`
	The skew factor, aka error in the XY pair (xyerr/xylen)

`--yzerr`
	Error in the Y-axis for the YZ pair in mm. (This argument cannot be used with "yzskew")

`--yzlen`
	Length of the test cube side where the "yzerr" measurement was taken.

`--yzskew`
	The skew factor, aka error in the YZ pair (yzerr/yzlen).

`--xzerr`
	Error in the Z-axis for the XZ pair in mm. (This argument cannot be used with "xzskew")

`--xzlen`
	Length of the test cube side where the "xzerr" measurement was taken.

`--xzskew`
	The skew factor, aka error in the XZ pair (xzerr/xzlen).

`--overwrite`
    Overwrite the input file with the skewed version. Useful for slicer post-processing.

`--verbose`
    Increases terminal output verbosity.