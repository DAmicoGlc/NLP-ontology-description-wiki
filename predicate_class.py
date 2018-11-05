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

class predicate(object):

	## METHODS

	# builder
	def __init__(self,predicateName,predicateType):

		# value of predicate name
		self.predicateName = predicateName
		
		# value of predicate ontology type
		self.predicateType = predicateType

		# list of superToken which form the predicate
		self.predicateSuperTokenList = None


	## GET METHODS
	

	# method to get predicate name
	def getName(self):
		return self.predicateName

	# method to get predicate type
	def getType(self):
		return self.predicateType

	# method to get list of predicatSuperToken
	def getSuperTokenList(self):
		return self.predicateSuperTokenList

	# method to get mapping string
	def getMapString(self,tokenSequence):
		return tokenSequence+"->"+self.predicateName


	## SET METHODS


	# method to set predicate name
	def setName( self,predicateName ):
		self.predicateName = predicateName

	# method to set predicate type
	def setType( self,predicateType ):
		self.predicateType = predicateType

	# method to set list of superToken
	def setSuperTokenList( self,predicateSuperTokenList ):
		self.predicateSuperTokenList = predicateSuperTokenList


	## SUPPORT METHODS

	# method to add a superToken to the list
	def addSuperToken( self,superToken ):
		predicateSuperTokenList.append(superToken)

	# method to string
	def toString(self):
		return "["+self.predicateType+"]["+self.predicateName+"]"