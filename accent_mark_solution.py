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

from operation_file import rewriteFilePredicateTaggerTree , readFileFromTaggerTree
from execution_tagger import exeTagger

# define a method to solve accent mark problem
def executeTaggerTreeunknown (tokenList,stopWordList):

	# define input and output file name
	inputFile = "accentSolution/file_input_accent_predicate.txt"
	outputFile = "accentSolution/file_output_accent_predicate.txt"

	# change token which has "<unknown>" as lemma adding the accent mark
	newTokenList = addAccentunknown(tokenList)

	# call tagger tree on new list
	accentTokenList = updateFileTagger(newTokenList,inputFile,outputFile,stopWordList)

	# check if there are "<unknown>" left
	returnedDictionary = removeAccentiunknown(accentTokenList,tokenList)

	# return dictionary
	return returnedDictionary



# define method to update file fo taggerTree program
def updateFileTagger (tokenList,inputFile,outputFile,stopWordList):

	# recall taggerTree program on new token list and check the result, all found "<unknown>" will be return to their origin form
	# recreate file with a new list
	rewriteFilePredicateTaggerTree(tokenList,inputFile)

	# recall TaggerTree program overwriting old file
	exeTagger(inputFile,outputFile)

	# extract result from the file
	newFeaturesList = readFileFromTaggerTree(outputFile,stopWordList)

	return newFeaturesList


# method to modify accent mark
def addAccentunknown (tokenList):

	newTokenList = tokenList[:]

	# for each token
	for token in newTokenList:

		# extract index of current token
		tokenIndex = newTokenList.index(token)

		# extract last character
		lastCharacter = token[len(token)-1]

		if lastCharacter == 'a':
			# modify last character adding accent mark
			newToken = token[:len(token)-1]+u'à'
			# modify list with new token
			newTokenList[tokenIndex] = newToken
		elif lastCharacter == 'e':
			# modify last character adding accent mark
			newToken = token[:len(token)-1]+u'è'
			# modify list with new token
			newTokenList[tokenIndex] = newToken
		elif lastCharacter == 'i':
			# modify last character adding accent mark
			newToken = token[:len(token)-1]+u'ì'
			# modify list with new token
			newTokenList[tokenIndex] = newToken
		elif lastCharacter == 'o':
			# modify last character adding accent mark
			newToken = token[:len(token)-1]+u'ò'
			# modify list with new token
			newTokenList[tokenIndex] = newToken
		elif lastCharacter == 'u':
			# modify last character adding accent mark
			newToken = token[:len(token)-1]+u'ù'
			# modify list with new token
			newTokenList[tokenIndex] = newToken

	return newTokenList


# define method to remove accent mark added
def removeAccentiunknown (predicateSuperTokenList,oldTokenList):

	newFeaturesDictionary = {}

	accentList = predicateSuperTokenList[0]

	index = 0

	# looking for what token has <unknown> value in the list
	for superToken in accentList:

		# if lemma is unknown
		if superToken.getLemma() == '<unknown>':

			# add old token as lemma in dictionary
			newFeaturesDictionary[oldTokenList[index]] = oldTokenList[index]

		else:
			
			# add lemma in dictionary
			newFeaturesDictionary[oldTokenList[index]] = superToken.getLemma()

		index = index+1

	return newFeaturesDictionary