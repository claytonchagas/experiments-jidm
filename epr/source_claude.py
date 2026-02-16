#!/usr/bin/env python
#    Simple EPR simulation
#    Copyright (C) 2015  Michel Fodje
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import division
import numpy
import sys
import time
import gzip
import os

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: \n\t source.py <duration in seconds> <spin>\n")
    else:
        if len(sys.argv) == 3:
            spin = float(sys.argv[2])
        else:
            spin = 1.0
        duration = float(sys.argv[1])

        left = []
        right = []
        n = 2*spin
        phase = n*numpy.pi
        angles = numpy.linspace(0, 2*numpy.pi, 33)
        ps = 0.5*numpy.sin(numpy.linspace(0, numpy.pi/2, 1000))**2

        start_t = time.time()
        print("Generating particle spin-{0} particle pairs".format(n*0.5))
        count = 0
        while time.time() - start_t <= duration:
            e = numpy.random.choice(angles)
            p = numpy.random.choice(ps)
            left.append(numpy.array([e, p, n]))
            right.append(numpy.array([e+phase, p, n]))
            count += 1
            sys.stdout.write("\rETA: %4ds [%8d pairs generated]" % (duration - time.time() + start_t, count))
            sys.stdout.flush()

        fname = 'SrcLeft.npy.gz'
        a = numpy.array(left)
        f = gzip.open(fname, 'wb')
        numpy.save(f, a)
        f.close()

        fname = 'SrcRight.npy.gz'
        a = numpy.array(right)
        f = gzip.open(fname, 'wb')
        numpy.save(f, a)
        f.close()

        print()
        print("%d particles in 'SrcLeft.npy.gz'" % (len(left)))
        print("%d particles in 'SrcRight.npy.gz'" % (len(right)))