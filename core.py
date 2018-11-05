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

# CORE MODULE

# import module

from operation_file import readFileFromTaggerTree , writeFileForTaggerTree , readCTSV , readOWLXML , readConfig , readOneListCTSV
from tokenizer import tokenizeDescription , tokenizePredicate
from predicate_class import predicate
from supertoken_class import superToken , predicateSuperToken
from predicate_node_class import predicateNode
from execution_tagger import exeTagger
from accent_mark_solution import executeTaggerTreeunknown
from tree_creation import buildPredicateDictionaryTree
from research_algorithm import findPredicates

import sys , os
import fnmatch

# define main method
# input main
# - config file
# - input file predicate
# - input file description
# - predicate delimiter
# - stopWordList
# - accentProblem True if there is not accent mark in predicate
def core( configFile="config.txt" , accentProblem=True , predicateInputFile="" , stopWordList=[] , descriptionInputFile="" , inputDescription=None , predicateDelimiter=None ):

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
		accentDictionary = {"citta":"città"}

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

	resultList = []

	failList = []

	splittedFileName = descriptionInputFile.split('.')

	# check if desctiptions are stored in .tsv file
	if splittedFileName[ len(splittedFileName)-1 ] == "tsv" :

		# extract description and predicate
		resultList = readOneListCTSV( descriptionInputFile,"descrption" )

		# save list of description
		descriptionList = resultList[0]

		# extract failed list
		failList = resultList[1]

		if len(failList) > 0:
			# write failed description in a file
			writeDescriptionList(failList,"fail")
	else:
		# otherwise descriptions are stored in .csv file

		# extract description and predicate
		resultList = readOneListCTSV( descriptionInputFile,"descrption",";" )

		# extract list of description
		descriptionList = resultList[0]

		# extract failed list
		failList = resultList[1]

		if len(failList) > 0:
			# write failed description in a file
			writeDescriptionList(failList,"fail")

	splittedFileName = predicateInputFile.split('.')

	# check if predicates are stored in .tsv file
	if splittedFileName[ len(splittedFileName)-1 ] == "tsv" :

		# extract description and predicate
		resultList = readOneListCTSV( predicateInputFile,"predicate" )

		# extract list of description
		predicateList = resultList[0]

		# extract failed list
		failList = resultList[1]

		if len(failList) > 0:
			# write failed description in a file
			writeDescriptionList(failList,"fail")

	# otherwise check if predicates are stored in .csv file
	elif splittedFileName[ len(splittedFileName)-1 ] == "csv" :

		# extract description and predicate
		resultList = readOneListCTSV( predicateInputFile,"predicate",";" )

		# extract list of description
		predicateList = resultList[0]

		# extract failed list
		failList = resultList[1]

		if len(failList) > 0:
			# write failed description in a file
			writeDescriptionList(failList,"fail")

	# otherwise predicates are stored in .owl file
	else:

		# extract description and predicate
		predicateList = readOWLXML( "file://"+predicateInputFile )


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

		# predicate counter
		numPredicate = 0

		# list of mapping
		mappedToken = []

		# for each predicate in list
		for predicate in predicateTokenList:

			# for each token in predicate
			for token in predicate:

				# check if it is in map dictionary
				if token in mapDictionary:

					# save token changed
					mappedToken.append("Number predicate: "+numPredicate+" Mapping: "+token+" into "+mapDictionary[ token ])

					# change it with map value with that key
					token = mapDictionary[ token ]

			numPredicate = numPredicate + 1

		# write changed list in file
		writePredicateList( mappedToken,"mapUpdate" )

	# check if accent problem is true
	if accentProblem:

		# for each predicate in list
		for predicate in predicateTokenList:

			# for each token in predicate
			for token in predicate:

				# check if it is in accent dictionary
				if token in accentDictionary:

					# change it with accented value with that key
					token = accentDictionary[ token ]

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
	exeTagger( descriptionFileName,fileNameOutput)

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

		# write list of changed lemma
		writePredicateList( unknownList,"unknownList" )

		# apply solution
		newLemmaDictionary = executeTaggerTreeunknown(unknownList,stopWordList)

		unknownSolved = []

		# for each object in indexSuperTokenList
		for listOfIndex in indexSuperTokenList:

			# for each index in index superToken  
			for indexSuperToken in listOfIndex[1]:

				# extract predicate to change from predicateSuperToken 
				predicateToChange = predicateSuperTokenList[ listOfIndex[0] ][ indexSuperToken[0] ]

				# save changed
				unknownSolved.append("Pre solution = "+predicateToChange.getLemma()+" Post solution: "+newLemmaDictionary[predicateToChange.getToken()])

				# change lemma of predicate superToken changed
				predicateToChange.setLemma( newLemmaDictionary[predicateToChange.getToken()] )
	

	# write list of changed lemma
	writePredicateList( unknownSolved,"unknownSolved" )

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

	print ("Descrizioni taggate: ")
	for description in descriptionList:

		
		print (description["taggedDescription"])

		if description["ambiguity"]:

			for ambiguous in description["ambiguity"]:

				print ("----------Ambiguità riscontrata: ")
				print ("-----TokenSequence ambiguos: ")
				
				indexStart = ambiguous["indexStart"]
				offset = ambiguous["offSet"]
				tokenSequence = ""

				for index in range( indexStart , indexStart+offset+1 ):
					tokenSequence = tokenSequence + description["superTokenList"][index].getToken()+" "

				print (tokenSequence)

				print ("-----Possibili canidati: ")
				for candidate in ambiguous["candidateList"]:
					print (candidate.getName())

				print ("-----Candidato scelto: ")
				print (ambiguous["candidate"].getName())


	# save tagged description in file
	writeDescriptionList( descriptionList,"taggedDescription" )

	return descriptionList

# method to write description list after an operation
def writeDescriptionList( descList,listTypeName ):

	# flag to know if is a description or a sequence
	desc = False

	if listTypeName=="input":

		# file name saved
		fileName = "inputDescription.txt"

		# dictionary key
		key = "naturalDescription"

		# set flag
		desc = True

	elif listTypeName=="taggedDescription":

		# file name saved
		fileName = "taggedDescription.txt"

		# dictionary key
		key = "taggedDescription"

		# set flag
		desc = True

	# check flag
	if desc:

		# save fail dscription in a file
		# open file in write mode
		with open("log/"+fileName,"w") as file:

			# write each description in a line
			for description in descList:

				# write
				file.write(description[key]+"\n")
	else:

		# check list type
		if listTypeName=="tokenized":

			# save fail dscription in a file
			# open file in write mode
			with open("log/tokenizedDescription.txt","w") as file:

				# description each description in descList
				for description in descList:

					# write each token 
					for token in description["tokenizedDescription"]:

						# write
						file.write("--"+token)

					file.write("\n")

		elif listTypeName=="fail":

			# save fail dscription in a file
			# open file in write mode
			with open("log/failDescription.txt","w") as file:

				# write each description in a line
				for description in descList:

					for row in description:

						# write
						file.write(row+" ")

					# write
					file.write("\n")

		elif listTypeName=="superToken":
			# save fail dscription in a file
			# open file in write mode
			with open("log/superTokenDescription.txt","w") as file:

				# description each description in descList
				for description in descList:

					# write each token 
					for superToken in description["superTokenList"]:

						# write
						file.write("(("+superToken.getToken()+"--"+superToken.getLemma()+"--"+superToken.getchosenGroup()+"))")

					file.write("\n")

# method to write predicate list after an operation
def writePredicateList( predList,listTypeName ):

	isaList=False

	# check type of list
	if listTypeName=="mapUpdate":

		# name of file saved
		fileName = "mappedPredicate.txt"

		# flag
		isaList=True

	elif listTypeName=="unknownList":
		# name of file saved
		fileName = "unknownList.txt"

		# flag
		isaList=True

	elif listTypeName=="unknownSolved":
		# name of file saved
		fileName = "unknownSolved.txt"

		# flag
		isaList=True

	if isaList:

		# save fail dscription in a file
		# open file in write mode
		with open("log/"+fileName,"w") as file:

			# write each description in a line
			for string in predList:

				# write
				file.write(string+"\n")

	elif listTypeName=="input":

		# save fail dscription in a file
		# open file in write mode
		with open("log/inputPredicate.txt","w") as file:

			# write each description in a line
			for predicate in predList:

				# write
				file.write("Name="+predicate.getName()+"|Type="+predicate.getType()+"\n")

	elif listTypeName=="tokenized":

		# save fail dscription in a file
		# open file in write mode
		with open("log/tokenizedPredicate.txt","w") as file:

			# write each description in a line
			for predicate in predList:

				# foreach token in predicate
				for token in predicate:

					# write
					file.write("--"+token)

				file.write("\n")

	elif listTypeName=="superToken":

		# save fail dscription in a file
		# open file in write mode
		with open("log/superTokenPredicate.txt","w") as file:

			# write each predicate in predList
			for predicate in predList:

				# for each superToken in predicate
				for superToken in predicate:

					# write
					file.write("(("+superToken.getToken()+"--"+superToken.getLemma()+"--"+superToken.getchosenGroup()+"))")

				file.write("\n")

core()