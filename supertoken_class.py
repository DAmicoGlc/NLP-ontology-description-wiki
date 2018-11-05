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


class superToken(object):

	## METHODS

	# builder
	def __init__(self,token,lemma,chosenGroup,groupList):

		# value of initial token
		self.token = token

		# value of lemma related to token
		self.lemma = lemma

		# value of grammar group chosen for the token
		self.chosenGroup = chosenGroup

		# list of grammar group from which chosen one is selected
		self.groupList = groupList

		# boolean value to state if superToken is or not a StopWord 
		self.stopWord = False


	## CONTROL METHODS


	# methods to know if superToken is a stopWord
	def isaStopWord(self):
		return self.stopWord


	# method to know if superToken is a punctuation mark
	def isaPuntcuationMark(self):
		if self.chosenGroup in ["PON","SENT"]:
			return True
		else:
			return False


	## GET METHOD


	# method to get token of superToken
	def getToken(self):
		return self.token


	# method to get lemma of superToken
	def getLemma(self):
		return self.lemma


	# method to get chosenGroup of superToken
	def getchosenGroup(self):
		return self.chosenGroup


	# method to get groupList of superToken
	def getGroupList(self):
		return self.groupList


	## SET METHODS


	# method to set token of superToken
	def setToken( self,token ):
		self.token = token


	# method to set lemma of superToken
	def setLemma( self,lemma ):
		self.lemma = lemma


	# method to set chosenGroup of superToken
	def setchosenGroup( self,gruppo ):
		self.chosenGroup = gruppo


	# method to set groupList of superToken
	def setGroupList( self,gruppi ):
		self.groupList = gruppi


	# method to set groupList of superToken
	def setIsInStopWord( self,boolean ):
		self.stopWord = boolean

	# SUPPORT METHODS


	# method to set stopWord attribute
	def setIsaStopWord( self,stopWordList ):
		for stopWord in stopWordList:
			if stopWord.lower() in self.chosenGroup.lower():
				self.stopWord = True
			else:
				self.stopWord = False


	# method to have next token in list if it exists
	def nextIsaPunctuationMarkOrNull( self,lista ):
		if lista.index(self)+1 >= len(lista):
			# next == NULL
			return True
		else:
			if lista[lista.index(self)+1].isaPuntcuationMark():
				# next == punctuationMark
				return True
			else:
				return False

# predicateSuperToken subclass of superToken
class predicateSuperToken(superToken):

	## METHODS

	# builder
	def __init__(self,token,lemma,chosenGroup,groupList):

		# object reference to the predicate which is linked to predicateSuperToken
		self.linkedPredicate = None

		# boolean value to state that predicateSuperToken is a tail
		self.tail = False

		# superToken builder
		superToken.__init__(self,token,lemma,chosenGroup,groupList)

	## CONTROL METHODS
	

	# method to know that it is a tail
	def isaTail(self):
		return self.tail


	## GET METHODS


	# method to get predicate linked to predicateSuperToken
	def getPredicate(self):
		return self.linkedPredicate

	# method to get name of predicate linked to predicateSuperToken
	def getPredicateName(self):
		return self.linkedPredicate.getName()

	# method to get type of predicate linked to predicateSuperToken
	def getPredicateType(self):
		return self.linkedPredicate.getType()


	## SET METHODS


	# method to set name of predicate linked to predicateSuperToken
	def setPredicate( self,predicate ):
		self.linkedPredicate = predicate
		self.tail = True


	# method to set tail attribute, if predicateSuperToken is a tail of a predicate
	def setTail( self,boolean ):
		self.tail = boolean