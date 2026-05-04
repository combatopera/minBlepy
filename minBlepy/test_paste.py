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
from .minblep import MinBleps, Translator
from unittest import TestCase
import numpy as np

class TestPaste(TestCase):

    def _nocrash(self, outrate):
        naiverate = 250000
        minbleps = MinBleps.create(MinBleps.Params(naiverate, outrate, None))
        overflowsize = minbleps.overflowsize
        translator = Translator(naiverate, minbleps)
        for framecount in range(50, 200):
            diffbuf = np.empty(framecount, dtype = floatdtype) # TODO: Determinism.
            naivex, outcount = translator.step(framecount)
            outsize = outcount + overflowsize
            outbuf = np.empty(outsize, dtype = floatdtype)
            minbleps.paste(naivex, diffbuf, outbuf)

    def test_nocrash44100(self):
        self._nocrash(44100)

    def test_nocrash48000(self):
        self._nocrash(48000)
