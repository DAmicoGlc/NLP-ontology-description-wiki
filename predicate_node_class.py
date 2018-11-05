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

class predicateNode(object):

	## METHODS

	# builder
	def __init__(self,superToken):

		# object reference to superToken which is linked to predicate node
		self.superToken = superToken

		# dictionary which contains children of predicate node, keys are lemmas of superTokens associated to predicate node
		self.childDictionary = {}

		# boolean value to state if predicate node is a tail ( different from leaf concept )
		self.tail = False

		# value which contain other predicate superToken with same superTokenList in term of verbal tense
		# example: ha_residenza, aveva_residenza
		# the ambuigity going to be linked to tail node
		self.ambiguous = []

	## CONTROL METHODS
	

	# method to know if predicate node is a tail
	def isaTail(self):
		return self.tail


	# method to know if a key is in childDictionary
	def containNode( self,keyLemma ):
		if keyLemma in self.childDictionary:
			return True
		else:
			return False


	# method to know if predicate node has at least one child
	def haveChildren(self):
		if len(self.childDictionary) > 0:
			return True
		else:
			return False


	# method to know if predicate node is ambiguous
	def ambiguity(self):
		if len(self.ambiguous) > 0:
			return True
		else:
			return False


	## GET METHODS

	#  method to get child from dictionary related to keyLemma
	def getChild( self,keyLemma ):
		if keyLemma in self.childDictionary:
			return self.childDictionary[keyLemma]
		else:
			return ""


	# method to get node's predicateSuperToken
	def getSuperToken(self):
		return self.superToken


	# method to get children dicionary
	def getChildrenDictionary(self):
		return self.childDictionary


	# method to get mapping string if predicateSuperToken in node is a tail
	def getMapString(self,tokenSequence):
		if self.isaTail():
			return tokenSequence+" -> "+self.superToken.getPredicate()
		else:
			return ""

	# method to get ambiguity list
	def getAmbiguityList(self):
		return self.ambiguous


	## SET METHODS


	# method to mark the predicate node as a tail
	def setTail( self,boolean ):
		self.tail = boolean


	# method to set node's predicateSuperToken 
	def setSuperToken( self,superToken ):
		self.superToken = superToken


	# method to add child to node dictionary
	def addChild( self,childNode ):
		self.childDictionary[childNode.getLemma()]=childNode


	# method to add ambuiguity in predicate node
	def addAmbiguity( self,predicateSuperToken ):
		self.ambiguous.append(predicateSuperToken)