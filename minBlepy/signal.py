# Copyright 2014, 2020, 2026 Andrzej Cichocki and contributors

# This file is part of minBlepy.
#
# minBlepy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# minBlepy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with minBlepy.  If not, see <http://www.gnu.org/licenses/>.

from . import floatdtype, u4
from pyrbo import LOCAL, T, turbo
import numpy as np

class Osc:

    index = 0
    count = 0
    scale = 1

    def __init__(self, shape):
        self.shape = shape

    def __call__(self, v):
        self.index, self.count = self.chunk(len(self.shape), len(v), v)

    @turbo(types = dict(self = dict(index = u4, count = u4, scale = u4, shape = [T]), shapelen = u4, vlen = u4, v = [T]), dynamic = True)
    def chunk(self, shapelen, vlen, v):
        self_index = self_count = self_scale = self_shape = LOCAL
        while vlen > 0:
            if self_count >= self_scale:
                self_index = (self_index + 1) % shapelen
                self_count = 0
            v[0] = self_shape[self_index]
            v += 1
            vlen -= 1
            self_count += 1
        return self_index, self_count

class PCMSignal:

    dc = 0
    naivex = 0

    def __init__(self, minbleps, naivesignal):
        self.carry = np.zeros(minbleps.overflowsize, dtype = floatdtype)
        self.minbleps = minbleps
        self.naivesignal = naivesignal

    def __call__(self, v):
        naiven = self.minbleps.getminnaiven(self.naivex, len(v))
        u = np.empty(naiven, dtype = floatdtype)
        self.naivesignal(u)
        d = u.copy()
        d[0] -= self.dc
        d[1:] -= u[:-1]
        w = np.empty(len(v) + len(self.carry), dtype = floatdtype)
        w[:len(self.carry)] = self.carry
        w[len(self.carry):] = self.dc
        self.minbleps.paste(self.naivex, d, w)
        v[:] = w[:len(v)]
        self.carry[:] = w[len(v):]
        self.dc = u[-1]
        self.naivex = (self.naivex + naiven) % self.minbleps.naiverate
