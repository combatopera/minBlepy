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
from .signal import Osc
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
