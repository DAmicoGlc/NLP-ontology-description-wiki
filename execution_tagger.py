# -*- coding: utf-8 -*-
# Copyright © 2017 Gianluca D'Amico
# University La Sapienza Rome, Latina, Italy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess

# define method to execute the TaggerTree as an external process
def exeTagger(nameFileInput,nameFileOutput,parameterName='postagger/italian-utf8.par'):


	##TODO try catch in caso di errore che fare???

	# execute the sub process
	subprocess.call('postagger/bin/tree-tagger -lemma -proto -token '+parameterName+' '+nameFileInput+' '+nameFileOutput,shell=True)

