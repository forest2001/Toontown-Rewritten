#!/usr/bin/env python2

# This is an extremely simple script; no sophistication whatsoever.

import os
import sys

if len(sys.argv) < 3:
    print('Usage: %s resources phase_out' % sys.argv[0])
    sys.exit(1)

source = sys.argv[1]
dest = sys.argv[2]

if not os.path.exists(dest) or os.listdir(dest):
    print('Destination must be an empty directory!')
    sys.exit(1)

for d in os.listdir(source):
    phase = os.path.join(source, d)
    if not os.path.isdir(phase): continue
    out = os.path.join(dest, d+'.mf')

    os.system('multify -c -f %s %s' % (out, phase))
