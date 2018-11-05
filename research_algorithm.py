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

from predicate_class import predicate
from predicate_node_class import predicateNode
from supertoken_class import predicateSuperToken

# define method to find predicates in a description
# - superTokenList is the tokenize description
# - predicateDictionary is dictionay which contain predicates trees
def findPredicates( superTokenList , predicateDictionary ):

	# initialize description which is returned
	newDescription = ""

	# initialize mapping which is returned
	mappingTag = []

	# initialize ambiguity list which is returned
	ambiguityList = []

	# initialize predicate founded list which is returned
	foundedList = {}

	# extract length of the list
	listLen = len(superTokenList)

	# index to parse the list
	indexList = 0

	# start loop into the list
	while indexList < listLen :

		# extract current superToken
		currentSuperToken = superTokenList[ indexList ]

		# check if current superToken is a stopWord
		if currentSuperToken.isaStopWord() :

			# add to description current token
			newDescription = newDescription + currentSuperToken.getToken() + " "

			# go on next superToken in list
			indexList = indexList+1
		else:
			# otherwise start the research

			# check if lemma of superToken is not a predicateDicionary's key
			if currentSuperToken.getLemma() not in predicateDictionary:

				# add current token to description 
				newDescription = newDescription + currentSuperToken.getToken() + " "

				# go on next superToken in list
				indexList = indexList+1
			else:
				# otherwise keep on searching into the tree

				# initialize candidate 
				candidate = None

				# initialize candidate ambiguity
				candidateAmbiguos = False

				# initialize index from which candidate start
				indexCandidateStart = superTokenList.index(currentSuperToken)

				# initialize variable which define how many token the candidate has
				offSet = 0

				# extract root node from which start candidate research
				currentNode = predicateDictionary[currentSuperToken.getLemma()]

				# initialize variable to know when stop the research
				stopFind = False

				# initialize variable to parse internal tree of dictionary
				analyzedSuperToken = currentSuperToken

				# loop into tree untill one of this event happend
				# - currentNode have no child
				# - analyzedSuperToken is not a key of ChildrenDictionary of currentNode
				# - analyzedSuperToken is NULL ( end of list ) or a punctuation mark 
				while not stopFind:

					# check if node is a tail ( last token of a predicate )
					if currentNode.isaTail():

						# save possile candidate
						candidate = currentNode.getSuperToken().getPredicate()

						# save current offset
						offSetCandidate = offSet

						# check if node is ambiguos
						if currentNode.ambiguity():

							# save ambiguity
							candidateAmbiguos = True

							# save ambiguos list
							ambiguosList = currentNode.getAmbiguityList()

					# extract index of analyzedSuperToken
					analyzedIndex = superTokenList.index(analyzedSuperToken)

					# check if currentNode have children and if next superToken of analyzedSuperToken is not NULL and if is not a punctuation mark 
					if currentNode.haveChildren() and not analyzedSuperToken.nextIsaPunctuationMarkOrNull( superTokenList ) :

						# extract next superToken
						nextAnalyzedSuperToken = superTokenList[analyzedIndex+1]

						# check if nextAnalyzedSuperToken is not a stopWord
						if not nextAnalyzedSuperToken.isaStopWord() :

							# go on nextAnalyzedSuperToken
							analyzedSuperToken = nextAnalyzedSuperToken

							# check if analyzedSuperToken is not a key of childrenDictionary of current node
							if not currentNode.containNode(analyzedSuperToken.getLemma()) :

								# if it is stop research
								stopFind = True
							else:
								# otherwise go on next one superToken
								# increase offSet
								offSet=offSet+1

								# go on node which have lemma of analyzedSuperToken as a key
								currentNode = currentNode.getChild(analyzedSuperToken.getLemma())

								# go on research
						else:
							# otherwise ignore nextAnalyzedSuperToken extracting it without changing node
							analyzedSuperToken = nextAnalyzedSuperToken

							# increase offSet
							offSet=offSet+1

							# go on research
					else:
						# otherwise stop research because current node have no children or list is finshed or next superToken is a punctuation mark
						stopFind = True

				# check if a candidate was found
				if candidate != None:

					# check if candidate is ambiguos
					if candidateAmbiguos:

						# manage ambiguity
						betterCandidate = manageAmbiguity( candidate,offSetCandidate,indexCandidateStart,superTokenList,ambiguosList )

						# check if better candidate is not None
						if betterCandidate != None:

							supportList = ambiguosList[:]
							supportList.append(candidate)

							# append reference to token sequence , ambiguity list with slice so it can be changed without changing ambiguous list, and the candidate choosen
							ambiguityList.append( { "indexStart":indexCandidateStart , "offSet":offSetCandidate , "candidateList":supportList , "candidate":betterCandidate } )

							# change candidateand save the ambiguity to return it
							candidate = betterCandidate
						else:
							# otherwise

							supportList = ambiguosList[:]
							supportList.append(candidate)

							# append reference to token sequence , ambiguity list with slice so it can be changed without changing ambiguous list, and the candidate choosen
							ambiguityList.append( { "indexStart":indexCandidateStart , "offSet":offSetCandidate , "candidateList":supportList , "candidate":candidate } )

					# check if candidate was already founded
					if candidate.getName() in foundedList:

						# number of already founded predicate with this name
						numFounded = foundedList[candidate.getName()]

						# increase nuber of occurancy
						# foundedList[candidate.getName()] = numFounded + 1

						# go on research from token over the offset
						indexList = indexCandidateStart + offSetCandidate + 1

						tokenSequence = ""

						# add token to description
						for i in range(0,offSetCandidate):
							# add token
							tokenSequence = tokenSequence+superTokenList[indexCandidateStart + i].getToken()+" "

						# add last token
						tokenSequence = tokenSequence+superTokenList[indexCandidateStart + offSetCandidate].getToken()

						# insert string in description
						newDescription = newDescription+tokenSequence+" "
					else:
						# create a new key of the list
						foundedList[candidate.getName()] = 1 

						# save new description
						if superTokenList[indexCandidateStart+ offSetCandidate].isaStopWord():
							offSetCandidate = offSetCandidate - 1
						# create string to insert in description
						stringList = extractStringOfPredicate( candidate,offSetCandidate,indexCandidateStart,superTokenList )

						# insert string in description
						newDescription = newDescription+stringList[0]

						# add change to mappingList
						mappingTag.append( [candidate.getMapString(stringList[1]) ,indexCandidateStart,indexCandidateStart+offSetCandidate ] )

						# go on research from token over the offset
						indexList = indexCandidateStart + offSetCandidate + 1
				else:
					# otherwise go on research from next token
					# insert current token in description
					newDescription = newDescription+currentSuperToken.getToken()+" "

					# go on next superToken
					indexList = indexList+1

	return [newDescription,mappingTag,ambiguityList,foundedList]


def extractStringOfPredicate( predicato,offset,startIndex,superList ):

	stringList = []

	stringList.append('[['+predicato.getType()+'|'+predicato.getName()+'|')

	tokenSequence = ""

	for i in range(0,offset):
		# add token
		tokenSequence = tokenSequence+superList[startIndex + i].getToken()+" "

	# add last token
	tokenSequence = tokenSequence+superList[startIndex + offset].getToken()

	stringList[0] = stringList[0]+tokenSequence+']]'+' '

	stringList.append(tokenSequence)

	return stringList

def manageAmbiguity( candidate,offSetCandidate,indexCandidateStart,superTokenList,ambiguosList ):

	ambiguosSuperTokenList = []

	# extract predicateSuperTokenList from ambiguosList
	for predicate in ambiguosList:
		ambiguosSuperTokenList.append( predicate.getSuperTokenList() )

	# define list of verbal tense
	presentTense = ["VER:pres","VER:cond","VER:cpre","VER:geru","VER:infi","VER:impe","VER:ppre","VER:pper"]
	pastTense = ["VER:impf","VER:cimp","VER:remo","VER:ppre"]
	futureTense = ["VER:futu"]

	differenceTense = []
	differenceTense.append({})

	# variable to know when stop while loop
	differenceFounded = False

	# for all ambiguos superToken, search why they are different in term of verbal tense
	for superToken in candidate.getSuperTokenList():

		# variable to parse all super token
		indexToken = 0

		# check if current superToken is a verb
		if "VER" in superToken.getchosenGroup():

			# for each superToken ambiguos
			while not differenceFounded:

				# variable to parse all super token
				indexAmbiguos = 0

				# for each ambiguosSuperTokenList in ambiguos list 
				for tokenList in ambiguosSuperTokenList:

					# check if verbal tense is different
					if superToken.getchosenGroup() != tokenList[indexToken].getchosenGroup():

						# if first elemet in list is empty
						if differenceTense[0] == {}:

							# save tense of candidate
							differenceTense[0] = {"tense":superToken.getchosenGroup()}

						differenceTense.append( {"tense":tokenList[indexToken].getchosenGroup(),"index":indexAmbiguos } )

						differenceFounded = True

						indexAmbiguos = indexAmbiguos+1

		indexToken = indexToken+1 

	betterCandidate = None


	# if it found some difference 
	if differenceFounded:

		index = 0

		# solve the difference
		# for each different probably candidate
		for tense in differenceTense:

			# check what is the tense of superToken in superTokenList
			if superTokenList[indexCandidateStart + indexToken-1].getchosenGroup() in presentTense and tense["tense"] in presentTense:

				# if is not first element
				if index != 0:

					# save better candidate
					betterCandidate = ambiguosList[tense["index"]]

			# check what is the tense of superToken in superTokenList
			if superTokenList[indexCandidateStart + indexToken-1].getchosenGroup() in pastTense and tense["tense"] in pastTense:

				# if is not first element
				if index != 0:

					# save better candidate
					betterCandidate = ambiguosList[tense["index"]]
					
			# check what is the tense of superToken in superTokenList
			if superTokenList[indexCandidateStart + indexToken-1].getchosenGroup() in futureTense and tense["tense"] in futureTense:

				# if is not first element
				if index != 0:

					# save better candidate
					betterCandidate = ambiguosList[tense["index"]]

			index = index + 1


	if betterCandidate != None:

		return betterCandidate

	else:

		return None
