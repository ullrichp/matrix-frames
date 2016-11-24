from __future__ import print_function

import argparse
import contextlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument('in_file_name')
parser.add_argument('-o', action='store', dest='out_file_name')

args = parser.parse_args()


@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


with smart_open(args.out_file_name) as outFile:
    with open(args.in_file_name, 'r') as inFile:
        lineNr = 1
        matrixStartLineNr = 0
        matrixEndLineNr = 0
        for line in inFile:

            if line.startswith('PAD:'):
                matrixStartLineNr = lineNr
                continue

            if matrixStartLineNr > 0 and line.startswith('FRAME:'):
                print('', file=outFile)
                matrixStartLineNr = 0
                continue

            if matrixStartLineNr > 0 and matrixStartLineNr + 2 <= lineNr and len(line) > 0 and line[0] != '\n':
                line = line.rstrip('\n')
                inValues = line.split(';')
                outValues = []
                for inValue in inValues:
                    outValues.append(inValue.replace('"', '').replace(',', '.'))

                print(' '.join(outValues), file=outFile)

            lineNr += 1
