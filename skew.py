#!/usr/bin/env python3
import re
import os
import argparse

parser = argparse.ArgumentParser(description='gskewer is a tool to skew the coordinates in a G-code file.')

xygroup = parser.add_mutually_exclusive_group(required=True)
xygroup.add_argument('--xyerr', type=float, help='Error in the X-axis for the XY pair in mm.')
xygroup.add_argument('--xytan', type=float, help='The error in the XY pair as a tangent. (xyerr/xylen)')


yzgroup = parser.add_mutually_exclusive_group(required=True)
yzgroup.add_argument('--yzerr', type=float, help='Error in the Y-axis for the YZ pair in mm.')
yzgroup.add_argument('--yztan', type=float, help='The error in the YZ pair as a tangent. (yzerr/yzlen)')


zxgroup = parser.add_mutually_exclusive_group(required=True)
zxgroup.add_argument('--zxerr', type=float, help='Error in the Z-axis for the ZX pair in mm.')
zxgroup.add_argument('--zxtan', type=float, help='The error in the ZX pair as a tangent. (zxerr/zxlen)')


parser.add_argument('--xylen', default=100, type=int, help='Length of the side where the XY error measurement was taken. This is optional, default value is 100mm')
parser.add_argument('--yzlen', default=100, type=int, help='Length of the side where the YZ error measurement was taken. This is optional, default value is 100mm')
parser.add_argument('--zxlen', default=100, type=int, help='Length of the side where the ZX error measurement was taken. This is optional, default value is 100mm')

# input file setup. name of input file is not in "args.file"
parser.add_argument("file", type=str)

#parser.add_argument('-v', action='count', help='Increases terminal output verbosity. More V's will increase verbosity' )

args = parser.parse_args()

if args.xytan:
	xytan = args.xytan
elif args.xyerr:
	xytan = args.xyerr/args.xylen
else:
	xytan = 0.0

if not xytan == 0:
	print('The XY error is set to', xytan,'degrees')

if args.yztan:
	yztan = args.yztan
elif args.yzerr:
	yztan = args.yzerr/args.yzlen
else:
	yztan = 0.0

if not yztan == 0:
	print('The YZ error is set to', yztan,'degrees')

if args.zxtan:
	zxtan = args.zxtan
elif args.zxerr:
	zxtan = args.zxerr/args.zxlen
else:
	zxtan = 0.0

if not zxtan == 0:
	print('The ZX error is set to', zxtan,'degrees')

if xytan == 0.0 and yztan == 0.0 and zxtan == 0.0:
	print('No skew parameters provided. Nothing will be done.')

filename = args.file

outname = re.sub(r'.gcode', '-skewed.gcode', filename)

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

            # load the incoming X coordinate into a variable. Previous value will be used if new value is not found.
            xsrch = re.search(r'[xX]\d*\.*\d*',line,re.I)
            if xsrch: # if an X value is found
                xin = float(re.sub(r'[xX]','',xsrch.group())) # Strip the letter from the coordinate.

            # load the incoming Y coordinate into a variable. Previous value will be used if new value is not found.
            ysrch = re.search(r'[yY]\d*\.*\d*', line, re.I)
            if ysrch:
                yin = float(re.sub(r'[yY]','',ysrch.group())) # Strip the letter from the coordinate.

            # load the incoming Z coordinate into a variable. Previous value will be used if new value is not found.
            zsrch = re.search(r'[zZ]\d*\.*\d*', line, re.I)
            if zsrch:
                zin = float(re.sub(r'[zZ]','',zsrch.group())) # Strip the letter from the coordinate.

            # calculate the corrected/skewed XYZ coordinates
            xout = round(xin-yin*xytan,3)
            yout = round(yin-zin*yztan,3)
            zout = round(zin-xin*zxtan,3)

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
