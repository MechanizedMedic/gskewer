#!/usr/bin/env python3
import re
import os
import argparse

parser = argparse.ArgumentParser(
    description='gskewer is a tool to skew the coordinates in a G-code file.'
)

xygroup = parser.add_mutually_exclusive_group(required=True)
xygroup.add_argument(
    '--xyerr',
    type=float,
    help='Error in the X-axis for the XY pair in mm.'
)
xygroup.add_argument(
    '--xyskew',
    type=float,
    help='The skew factor, aka error in the XY pair (xyerr/xylen)'
)


yzgroup = parser.add_mutually_exclusive_group(required=True)
yzgroup.add_argument(
    '--yzerr',
    type=float,
    help='Error in the Y-axis for the YZ pair in mm.'
)
yzgroup.add_argument(
    '--yzskew',
    type=float,
    help='The skew factor, aka error in the yz pair (yzerr/yzlen).'
)


zxgroup = parser.add_mutually_exclusive_group(required=True)
zxgroup.add_argument(
    '--zxerr',
    type=float,
    help='Error in the Z-axis for the ZX pair in mm.'
)
zxgroup.add_argument(
    '--zxskew',
    type=float,
    help='The skew factor, aka error in the ZX pair (zxerr/zxlen).'
)


parser.add_argument(
    '--xylen',
    default=100,
    type=int,
    help='Length of the side where the XY error measurement was taken. This is optional, default value is 100mm'
)
parser.add_argument(
    '--yzlen',
    default=100,
    type=int,
    help='Length of the side where the YZ error measurement was taken. This is optional, default value is 100mm'
)
parser.add_argument(
    '--zxlen',
    default=100,
    type=int,
    help='Length of the side where the ZX error measurement was taken. This is optional, default value is 100mm'
)

# input file setup. name of input file is not in "args.file"
parser.add_argument("file", type=str)

parser.add_argument(
    '-o',
    '--overwrite',
    action='store_true',
    help='Overwrite the input file with the skewed version. Useful for slicer post-processing.'
)

parser.add_argument(
    '-v',
    '--verbose',
    action='count',
     help='Increases terminal output verbosity.'
)

args = parser.parse_args()

if args.xyskew:
    xyskew = args.xyskew
elif args.xyerr:
    xyskew = args.xyerr / args.xylen
else:
    xyskew = 0.0

if not xyskew == 0:
    print('The XY error is set to', xyskew)

if args.yzskew:
    yzskew = args.yzskew
elif args.yzerr:
    yzskew = args.yzerr / args.yzlen
else:
    yzskew = 0.0

if not yzskew == 0:
    print('The YZ error is set to', yzskew)

if args.zxskew:
    zxskew = args.zxskew
elif args.zxerr:
    zxskew = args.zxerr / args.zxlen
else:
    zxskew = 0.0

if not zxskew == 0:
    print('The ZX error is set to', zxskew)

if xyskew == 0.0 and yzskew == 0.0 and zxskew == 0.0:
    print('No skew parameters provided. Nothing will be done.')

filename = args.file

outname = re.sub(r'.gcode', '-skewed.gcode', filename)

xin = 0.0
yin = 0.0
zin = 0.0

if os.path.isfile(outname):
    os.remove(outname)

with open(outname, 'a') as outfile:
    with open(filename, 'r') as infile:
        for line in infile:
            # Check that the current 'line' is a move, if so the line is processed
            gmatch = re.match(r'G[0-1]', line, re.I)
            if gmatch:
                if args.verbose:
                    print('line was a G0/G1 command!')

                # load the incoming X coordinate into a variable. Previous value will be used if new value is not found.
                xsrch = re.search(r'[xX]-?\d*\.*\d*', line, re.I)
                if xsrch:  # if an X value is found
                    # Strip the letter from the coordinate.
                    xin = float(re.sub(r'[xX]', '', xsrch.group()))

                # load the incoming Y coordinate into a variable. Previous value will be used if new value is not found.
                ysrch = re.search(r'[yY]-?\d*\.*\d*', line, re.I)
                if ysrch:
                    # Strip the letter from the coordinate.
                    yin = float(re.sub(r'[yY]', '', ysrch.group()))

                # load the incoming Z coordinate into a variable. Previous value will be used if new value is not found.
                zsrch = re.search(r'[zZ]-?\d*\.*\d*', line, re.I)
                if zsrch:
                    # Strip the letter from the coordinate.
                    zin = float(re.sub(r'[zZ]', '', zsrch.group()))

                # calculate the corrected/skewed XYZ coordinates
                xout = round(xin - yin * xyskew, 3)
                yout = round(yin - zin * yzskew, 3)
                xout = round(xout - zin * zxskew, 3)
                # Z coodinates must remain the same to prevent layers being tilted!
                zout = zin

                lineout = line
                if args.verbose:
                    print('old line:', lineout)

                if xsrch:
                    lineout = re.sub(r'[xX]-?\d*\.*\d*', 'X' + str(xout), lineout)

                if ysrch:
                    lineout = re.sub(r'[yY]-?\d*\.*\d*', 'Y' + str(yout), lineout)

                if zsrch:
                    lineout = re.sub(r'[zZ]-?\d*\.*\d*', 'Z' + str(zout), lineout)

                if args.verbose:
                    print('new line: ', lineout)
                outfile.write(lineout)
            else:
                if args.verbose:
                    print('Skipping, not a movement.', line)
                outfile.write(line)

if args.overwrite:
    os.replace(outname, filename)