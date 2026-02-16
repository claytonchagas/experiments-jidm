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
import gzip
import time
import os


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: \n\t station.py <ArmSrcFile> seting1,setting2,setting3,...\n")
    else:
        if len(sys.argv) == 2:
            angles = numpy.linspace(0, 2*numpy.pi, 33)
        else:
            angles = numpy.radians(numpy.array(map(float, sys.argv[2].split(','))))
        particles = numpy.load(gzip.open(sys.argv[1], 'rb'))
        name = {'SrcLeft.npy.gz': 'Alice', 'SrcRight.npy.gz': 'Bob'}[sys.argv[1]]

        station_name = name
        station_particles = particles
        station_results = numpy.empty((len(station_particles), 2))
        station_default = numpy.nan

        print("Detecting particles for %s's arm" % station_name)
        st = time.time()
        infos = zip(particles, numpy.random.choice(angles, size=len(particles)))
        results = []
        for info in infos:
            particle, setting = info
            e, p, n = particle
            C = ((-1)**n)*numpy.cos(n*(setting-e))
            out = numpy.sign(C) if p < abs(C) else numpy.nan
            results.append([setting, out])
        print("Done: {0} particles detected in {1:5.1f} sec!".format(len(particles), time.time() - st))
        station_results = numpy.array(results)

        fname = "%s.npy.gz" % station_name
        f = gzip.open(fname, 'wb')
        numpy.save(f, station_results)
        f.close()