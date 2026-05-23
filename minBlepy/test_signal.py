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

from . import floatdtype
from .minblep import MinBleps
from .signal import Osc, PCMSignal
from collections import defaultdict
from unittest import TestCase
import numpy as np

class TestOsc(TestCase):

    def test_works(self):
        osc = Osc(np.array([1, 2, 3], dtype = floatdtype))
        osc.scale = 2
        v = np.empty(5, dtype = floatdtype)
        osc(v)
        self.assertEqual([1, 1, 2, 2, 3], list(v))
        osc(v)
        self.assertEqual([3, 1, 1, 2, 2], list(v))
        osc(v)
        self.assertEqual([3, 3, 1, 1, 2], list(v))
        osc.scale = 4
        osc(v)
        self.assertEqual([2, 2, 2, 3, 3], list(v))
        osc(v)
        self.assertEqual([3, 3, 1, 1, 1], list(v))
        osc.scale = 1
        osc(v)
        self.assertEqual([2, 3, 1, 2, 3], list(v))

class TestPCMSignal(TestCase):

    def test_spectrum(self):
        p = MinBleps.Params(100000, 8000)
        self.assertEqual(25, p.scale)
        square = Osc(np.array([1, -1], dtype = floatdtype))
        square.scale = 200
        tone = p.naiverate / (square.scale * len(square.shape))
        self.assertEqual(250, tone)
        mb = MinBleps.create(p)
        signal = PCMSignal(mb, square)
        nyq = 4096
        size = nyq * 2
        v = np.empty(size, dtype = floatdtype)
        signal(v[:1000])
        for i in range(1000, 2000, 5):
            signal(v[i:i + 5])
        signal(v[2000:])
        spectrum = np.abs(np.fft.fft(v * np.hanning(size), norm = "forward"))
        spectrum[1:nyq] += spectrum[size:nyq:-1]
        spectrum = spectrum[:nyq + 1]
        amp = defaultdict(lambda: 0)
        for i in range(1, nyq + 1):
            a = spectrum[i]
            if 20 * np.log10(a) > -90:
                f = i / size * p.outrate
                h = round(f / tone)
                self.assertEqual(1, h % 2)
                self.assertLess(abs(tone * h - f), 1)
                amp[h] += a
        for h, a in amp.items():
            if tone * h <= p.passband():
                self.assertLess(abs(amp[1] / h - a), .004)
