# Copyright 2014, 2020 Andrzej Cichocki

# This file is part of mynblep.
#
# mynblep is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mynblep is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mynblep.  If not, see <http://www.gnu.org/licenses/>.

from .util import atomic
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

class TestAtomic(TestCase):

    def test_works(self):
        for relpath in ['x'], ['x', 'y'], ['x', 'y', 'z']:
            with TemporaryDirectory() as d:
                p = Path(d, *relpath)
                for _ in range(2):
                    with atomic(p) as q, q.open('w') as f:
                        print('doc', file = f)
                    self.assertFalse(q.exists())
                    self.assertEqual('doc\n', p.read_text())
