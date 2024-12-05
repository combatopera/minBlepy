# Copyright 2014, 2020 Andrzej Cichocki and contributors

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

    def _works(self, outrate):
        naiverate = 250000
        minbleps = MinBleps.create(naiverate, outrate, None)
        overflowsize = minbleps.mixinsize
        translator = Translator(naiverate, minbleps)
        for framecount in range(50, 200):
            diffbuf = np.empty(framecount, dtype = floatdtype)
            naivex, outcount = translator.step(framecount)
            outsize = outcount + overflowsize
            outbuf = np.empty(outsize, dtype = floatdtype)
            minbleps.paste(naivex, diffbuf, outbuf)

    def test_44100(self):
        self._works(44100)

    def test_48000(self):
        self._works(48000)
