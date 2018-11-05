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

from predicate_node_class import predicateNode
from supertoken_class import predicateSuperToken


# function to build the dictionary of predicate as tree
def buildPredicateDictionaryTree ( predicateList ) :

	# output dictionaryTree of predicate
	predicateDictionaryTree = {}

	# loop on each predicate list of predicateSuperToken
	for predicateSuperTokenList in predicateList:

		# initialize current support dictionary to output dictionaryTree
		currentDictionary = predicateDictionaryTree

		# loop on each predicateSuperToken in predicate superToken list
		for predicateSuperToken in predicateSuperTokenList:	

			# pull out lemma from predicateSuperToken
			currentLemma = predicateSuperToken.getLemma()

			# check if current predicate superToken is not a stopWord
			if not predicateSuperToken.isaStopWord():

				# check if currentLemma is already a key of currentDictionary
				if currentLemma in currentDictionary:

					# initialize current node to node wich has currentLemma as a key
					currentNode = currentDictionary[currentLemma]

					# update currentDictionary as an internal children dictionary
					currentDictionary = currentNode.getChildrenDictionary()

					# check if predicateSuperToken is the last one in list, if it is a tail
					if predicateSuperToken.isaTail():
						# in that case check if current node is already a tail
						if currentNode.isaTail():
							# set node as ambiguos
							currentNode.addAmbiguity( predicateSuperToken.getPredicate() )
						else:
							# otherwise set node as a tail
							currentNode.setTail(True)

							# set superToken linked to node
							currentNode.setSuperToken( predicateSuperToken )

					# otherwise go on loop

				else:
					# else create a new predicate node with current predicateSuperToken
					newNode = predicateNode(predicateSuperToken)

					# add current lemma as a key of current dictionary
					currentDictionary[currentLemma] = newNode
					
					# update current node
					currentNode = newNode

					# check if added predicateSuperToken is the last predicateSuperToken in list
					if predicateSuperToken.isaTail():
						# mark node as tail
						currentNode.setTail(True)
					else:
						# otherwise update current dictionary as current node child dictionary
						currentDictionary = currentNode.getChildrenDictionary()

					# go on loop

			# otherwise go on loop to next predicate superToken


	# in the end, return the dictionary built
	return predicateDictionaryTree