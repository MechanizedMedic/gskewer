#!/usr/bin/env python3
import re
import os

# Define the tangent angles that will be used later
# This is the axis error from 90 degrees (measured in mm)
xyerr = 0.7
yzerr = 0.25
zxerr = 0.1

# length of the side where the error was measured (measured in mm)
xylen = 50
yzlen = 50
zxlen = 50

filename = 'H_Huntsman_Z_Mount.gcode'

outname = 'skewed-'+filename

xin = 0.0
yin = 0.0
zin = 0.0

if os.path.isfile(outname):
    os.remove(outname)

outfile = open(outname,'a')

with open(filename,'r') as infile:
    for line in infile:
        # Check that the current 'line' is a move, if so the line is processed
        gmatch = re.match(r'G[0-1]',line,re.I)
        if gmatch:
            print('line was a G0/G1 command!')

            # load the incoming X coordinate into a variable
            xsrch = re.search(r'[xX]\d*\.*\d*',line,re.I)
            if xsrch: # if an X value is found
                xin = float(re.sub(r'[xX]','',xsrch.group()))

            # load the incoming Y coordinate into a variable
            ysrch = re.search(r'[yY]\d*\.*\d*', line, re.I)
            if ysrch:
                yin = float(re.sub(r'[yY]','',ysrch.group()))

            # load the incoming Z coordinate into a variable
            zsrch = re.search(r'[zZ]\d*\.*\d*', line, re.I)
            if zsrch:
                zin = float(re.sub(r'[zZ]','',zsrch.group()))

            # calculate the corrected/skewed XYZ coordinates
            xout = round(xin-yin*(xyerr/xylen),3)
            yout = round(yin-zin*(yzerr/yzlen),3)
            zout = round(zin-xin*(zxerr/zxlen),3)

            lineout = line
            print('old line:', lineout)

            if xsrch:
                lineout = re.sub(r'[xX]\d*\.*\d*', 'X' + str(xout), lineout)

            if ysrch:
                lineout = re.sub(r'[yY]\d*\.*\d*', 'Y' + str(yout), lineout)

            if zsrch:
                lineout = re.sub(r'[zZ]\d*\.*\d*', 'Z' + str(zout), lineout)

            print('new line: ', lineout)
            outfile.write(lineout)
        else:
            print('Skipping, not a movement.', line)
            outfile.write(line)