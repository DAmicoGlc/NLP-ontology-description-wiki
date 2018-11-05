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

# TEST MODULE

# import module

from operation_file import readFileFromTaggerTree , writeFileForTaggerTree , readCTSV , readOWLXML , readConfig , readOneListCTSV
from tokenizer import tokenizeDescription , tokenizePredicate , tokenizeTestDescription
from predicate_class import predicate
from supertoken_class import superToken , predicateSuperToken
from predicate_node_class import predicateNode
from execution_tagger import exeTagger
from accent_mark_solution import executeTaggerTreeunknown
from tree_creation import buildPredicateDictionaryTree
from research_algorithm import findPredicates

import sys , os
import fnmatch

# method to write predicate list after an operation
def writePredicateList( predList,listTypeName ):
	return False

# method to write description list after an operation
def writeDescriptionList( descList,listTypeName ):
	return False


# define main method
# input main
# - config file
# - input file predicate
# - input file description
# - predicate delimiter
# - stopWordList
def main( configFile="config.txt" , accentProblem=True , predicateInputFile="" , stopWordList=[] , descriptionInputFile="" , inputDescription=None , predicateDelimiter=None ):

	### read configuration file
	# It is possible to choose some configuration information as:
	# - If there are some trick solution in predicate list, example write "est" instead of "è" for some implementation reason it is possible 
	#	to specify it in configuration file in the form est->è , so the core will change it
	# - Have to specify the predicate file name in input
	# - Have to specify the description name file in input, but it is possible to pass a single description as input in main method
	# - Have to specify wich character delimite the predicate word
	configurationList = readConfig( configFile )

	# if there is accent mark problem, define a dictionary of word to change
	if accentProblem:

		# word which have a pos tag without accent mark
		accentDictionary = {"citta":"città", "d'":"di"}

	### save results in variable for each configuration information extract from file
	
	# save mapping dictionary to changing some value in predicate list
	mapDictionary = configurationList[0]

	# save stopWord list to know if there are stop words 
	stopWordList = configurationList[1]

	# check if predicate input file is given in input of main
	if predicateInputFile == "":

		# then have to extract it from cinfiguration file
		# save the input file type of predicates
		predicateInputFile = configurationList[2]

	# check if description input file is given in input of main
	if descriptionInputFile == "":

		# then have to extract it from cinfiguration file
		# save the input file type of descriptions
		descriptionInputFile = configurationList[3]

	# check if input delimiter is ""
	if predicateDelimiter == "":
		# save delimiter character of predicate
		predicateDelimiter = configurationList[4]

	### extract description and predicate from input file

	descriptionList = []

	predicateList = []

	resultList = []

	failList = []

	splittedFileName = descriptionInputFile.split('.')

	# extract predicates and descriptions from tsv file
	resultList = readCTSV( "PROVATEST.tsv" )

	# extract description list from result
	descriptionList = resultList[0]

	# extract predicate list from result
	predicateList = resultList[1]

	# extract fail list from result
	failList = resultList[2]

	# write description list recived in input
	writeDescriptionList( descriptionList,"input" )

	# write predicate list recived in input
	writePredicateList( predicateList,"input" )

	### process predicate and description in input

	## tokenize it

	# tokenize description
	for description in descriptionList:

		# save tokenize description
		description["tokenizedDescription"] = tokenizeDescription( description["naturalDescription"] )

	# tokenize predicate in the list
	# pass predicate list as paramater in tokenize method
	predicateTokenList = tokenizePredicate( predicateList,predicateDelimiter )

	# write tokenized list of description in file
	writeDescriptionList( descriptionList,"tokenized" )

	# write tokenized list of predicate in file
	writePredicateList( predicateTokenList,"tokenized" )

	### change predicate if there are some map changing

	# check if mapDictionary is not empty
	if not len(mapDictionary) == 0:

		# for each predicate in list
		for predicate in predicateTokenList:

			# for each token in predicate
			for token in predicate:

				# check if it is in map dictionary
				if token in mapDictionary:

					# change it with map value with that key
					predicate[ predicate.index(token) ] = mapDictionary[ token ]

		# write changed list in file
		writePredicateList( predicateTokenList,"mapUpdate" )

	# check if accent problem is true
	if accentProblem:

		# for each predicate in list
		for predicate in predicateTokenList:

			# for each token in predicate
			for token in predicate:

				# check if it is in accent dictionary
				if token.lower() in accentDictionary:

					# extract index
					indexPred = predicateTokenList.index(predicate)

					indexToken = predicate.index(token)

					# change it with accented value with that key
					predicateTokenList[indexPred][indexToken] = accentDictionary[ token.lower() ]


	### pos tagging
	## before giving token list to pos tagger , have to write it in a file, with 1 toke for each line

	# write description in a file
	descriptionFileName = writeFileForTaggerTree( descriptionList,"description" )

	# write predicate in a file
	predicateFileName = writeFileForTaggerTree( predicateTokenList,"predicate" )

	## execute pos tagger for each predicates and for each descriptions and read the results

	# execute pos tagger for each predicate

	# define file name for the ouput
	fileNameOutput = "outputFile_tagger/file_output_traggerTree_predicate.txt"

	# execute pos tagger
	exeTagger( predicateFileName,fileNameOutput )

	# read output file from pos tagger
	predicateSuperTokenList = readFileFromTaggerTree(fileNameOutput,stopWordList) 

	# execute pos tagger for each description

	# define file name for the ouput
	fileNameOutput = "outputFile_tagger/file_output_traggerTree_description.txt"

	# execute pos tagger
	exeTagger(descriptionFileName,fileNameOutput)

	# read output file from pos tagger
	taggerTreeDescriptionList = readFileFromTaggerTree(fileNameOutput,stopWordList,descriptionList)

	# write results in a file
	writePredicateList( predicateSuperTokenList,"superToken" )
	writeDescriptionList( descriptionList,"superToken" )

	## it is possible that the accent mark is not present in predicate, so check for it with a brutal solution

	unknownList = []

	indexSuperTokenList = []

	# for each predicate in which there are some unknown lemma in some token
	for superTokenList in predicateSuperTokenList:
		
		indexSuperToken = []

		# for each superToken in list
		for superToken in superTokenList:

			# check if lemma of superToken is unknown
			if superToken.getLemma() == "<unknown>":

				# append it in a list of uknow token
				unknownList.append(superToken.getToken())

				# save it
				indexSuperToken.append( [superTokenList.index(superToken), len(unknownList)-1] )

		# check if an unknown is founded
		if len(indexSuperToken) > 0:

			# append index of superToken list in indexList
			indexSuperTokenList.append( [predicateSuperTokenList.index(superTokenList),indexSuperToken] )

	# if unknownList is not empty
	if len(unknownList) > 0:

		# apply solution
		newLemmaDictionary = executeTaggerTreeunknown(unknownList,stopWordList)

		# for each object in indexSuperTokenList
		for listOfIndex in indexSuperTokenList:

			# for each index in index superToken  
			for indexSuperToken in listOfIndex[1]:

				# extract predicate to change from predicateSuperToken 
				predicateToChange = predicateSuperTokenList[ listOfIndex[0] ][ indexSuperToken[0] ]

				# change lemma of predicate superToken changed
				predicateToChange.setLemma( newLemmaDictionary[predicateToChange.getToken()] )


	# write list of changed lemma
	writePredicateList( unknownList,"accentSolution" )

	### assign predicate to super token and viceversa

	# for each predicate save the relative superToken list
	for predicate in predicateList:

		# extract index of predicate
		predicateIndex = predicateList.index(predicate)

		# set superToken list
		predicate.setSuperTokenList( predicateSuperTokenList[predicateIndex] )

		# save the relative predicate in the last predicateSuperToken in list
		predicateSuperTokenList[predicateIndex][ len(predicateSuperTokenList[predicateIndex])-1 ].setPredicate(predicate)

	### create the tree structure for the research

	predicateDictionaryTree = buildPredicateDictionaryTree( predicateSuperTokenList )

	### start research

	tagMapping = []


	# for each description do the research
	for description in descriptionList:

		resultList = findPredicates( description["superTokenList"],predicateDictionaryTree )

		# extract tagged description
		description["taggedDescription"] = resultList[0]

		# extract tag mapping
		tagMapping.append(resultList[1])

		# extract ambiguity choice
		description["ambiguity"] = resultList[2]

		# extract predicate founded
		description["foundedPredicate"] = resultList[3]

		algorithmFounded = 0

		for founded in description["foundedPredicate"]:

			algorithmFounded = algorithmFounded + description["foundedPredicate"][founded]

		# extract number of predicate founde
		description["numberOfFounded"] = algorithmFounded



	#### TEST
	test = 1

	differenze = 0

	
	if test == 1:
		# for each description 
		for description in descriptionList:

			predicateTestFound = {}

			indexDesc = 0

			testFounded = 0

			tokenizeTest = tokenizeTestDescription(description["testTaggedDescription"])

			lenDesc = len(tokenizeTest)

			while indexDesc < lenDesc:
				
				if tokenizeTest[indexDesc] == '[':

					testFounded = testFounded +1 

					# jup to predicate [ [ type | predicate
					indexPredicate = indexDesc + 4

					inndexToken = indexDesc + 6
					
					numToken = 0
					try:
						while tokenizeTest[indexToken] != ']':

							numToken = numToken +1 
							
							indexToken = indexToken +1
					# in case of IndexError
					except IndexError as exception:
						# save row in failList
						numToken=0

					if numToken>0 :

						stringLen = tokenizeTest[indexPredicate].split("_")

						lenString = len(stringLen)


						if not lenString!=numToken:

							differenze = differenze +1	

					predicateTest = tokenizeTest[indexPredicate]

					if predicateTest in predicateTestFound:

						alreadyFounded = predicateTestFound[predicateTest]

						predicateTestFound[predicateTest] = alreadyFounded + 1

					else:
						predicateTestFound[predicateTest] = 1			

					indexDesc = indexDesc + 5

				indexDesc = indexDesc + 1

			description["testPredicateFound"] = predicateTestFound

			description["numberOfTestFounded"] = testFounded

		algorithmFounded = 0

		testFounded = 0

		for description in descriptionList:

			algorithmFounded = algorithmFounded + description["numberOfFounded"]

			testFounded = testFounded + description["numberOfTestFounded"]

		print ("Trovati da lui: ")
		print (testFounded)
		print ("Trovati da me: ")
		print (algorithmFounded)
		print ("Numero differnze")
		print (differenze)


		descIndex = 0

		numTruePos = 0
		numFalseNeg = 0
		numFalsePos = 0

		for description in descriptionList:

			description["truePositiveList"] = []

			truePredicate = []

			mapListTest = description["testPredicateFound"]

			mapListEvalueted = description["foundedPredicate"]

			truePositiveIndex = []

			for predicateTestFounded in mapListTest:

				if predicateTestFounded in mapListEvalueted:

					truePredicate.append(predicateTestFounded)

					if mapListTest[predicateTestFounded] > mapListEvalueted[predicateTestFounded]:

						numTruePos = numTruePos + mapListEvalueted[predicateTestFounded]

						numFalseNeg = numFalseNeg + ( mapListTest[predicateTestFounded] - mapListEvalueted[predicateTestFounded] )

					elif mapListTest[predicateTestFounded] < mapListEvalueted[predicateTestFounded]:

						numTruePos = numTruePos + mapListTest[predicateTestFounded]

						numFalsePos = numFalsePos + ( mapListEvalueted[predicateTestFounded] - mapListTest[predicateTestFounded] )
					else:

						numTruePos = numTruePos + mapListTest[predicateTestFounded]
				else:

					numFalseNeg = numFalseNeg + mapListTest[predicateTestFounded]

			for predicate in mapListEvalueted:

				if predicate not in truePredicate:

					numFalsePos = numFalsePos + mapListEvalueted[predicate]



		print ("True positive: "+str(numTruePos))
		print ("True negative: "+str(numFalseNeg))
		print ("False positive: "+str(numFalsePos))
	else:
		for description in descriptionList:

			print (description["testTaggedDescription"])
			print (description["taggedDescription"])

	
	print (predicateList[1].getName())
	print (descriptionList[1]["taggedDescription"])
	print (descriptionList[1]["testTaggedDescription"])

	# save tagged description in file
	writeDescriptionList( descriptionList,"taggedDescription" )




main()