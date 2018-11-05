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

import codecs
import csv
import sys
from owlready2 import *
from predicate_class import predicate
from supertoken_class import superToken , predicateSuperToken

# define method to read output file from the TaggerTree programm
def readFileFromTaggerTree(fileName,stopWordList,descriptionList=None):

	# define list which is returned
	classificationList = []

	# define list to return predicate list
	predicateSuperTokenList = []

	# define list to return description list
	descriptionSuperTokenList = []

	if "description" in fileName:

		lineNumber = 1

		indexDescription = 0

		lenDescLimit = len(descriptionList[indexDescription]["tokenizedDescription"])

		descriptionList[indexDescription]["superTokenList"] = []

	# open file which is read
	with codecs.open(fileName,'r',encoding='utf-8') as contentFile:

		# for each line in file
		for line in contentFile:

			# delete 'new line' character at the end of the file line
			line = line.rstrip()

			# replace blank with tab character
			line = line.replace(' ','\t')
			
			# create a list of string which contains the result of taggerTree for each token
			parameterList = line.split('\t')

			# check if in fourth parameter there is some choice
			if "|" in parameterList[2]:

				# take the first choice
				splittedParam = parameterList[2].split("|")

				# save it
				parameterList[2] = splittedParam[1]

			# check if it a predicate superToken or a normal one
			if "description" in fileName:

				# check if it is a delimiter
				if lineNumber < lenDescLimit:

					# create superToken for each line read
					newSuperToken = superToken( parameterList[0],parameterList[2],parameterList[1],parameterList[4] )

					# check and set if it is a stop word
					newSuperToken.setIsaStopWord(stopWordList)

					# append new superToken in the list
					descriptionList[indexDescription]["superTokenList"].append(newSuperToken)

					lineNumber = lineNumber + 1

				else:

					# create superToken for each line read
					newSuperToken = superToken( parameterList[0],parameterList[2],parameterList[1],parameterList[4] )

					# check and set if it is a stop word
					newSuperToken.setIsaStopWord(stopWordList)

					# append new superToken in the list
					descriptionList[indexDescription]["superTokenList"].append(newSuperToken)

					if indexDescription != len(descriptionList)-1:

						lineNumber = lineNumber + 1

						indexDescription = indexDescription + 1

						lenDescLimit = lenDescLimit + len(descriptionList[indexDescription]["tokenizedDescription"])

						descriptionList[indexDescription]["superTokenList"] = []

			else:

				# check if it is a punctuation mark
				if parameterList[0] != ".":

					if parameterList[1] == "<uknown>":

						# create predicateSuperToken for each line read
						newSuperToken = predicateSuperToken( parameterList[0].lower(),parameterList[2],parameterList[1],parameterList[4] )
					else:
						# create predicateSuperToken for each line read
						newSuperToken = predicateSuperToken( parameterList[0].lower(),parameterList[2],parameterList[1],parameterList[4] )

					# check and set if it is a stop word
					newSuperToken.setIsaStopWord(stopWordList)

					# append new superToken in the list
					predicateSuperTokenList.append(newSuperToken)
				else:
					# otherwise append predicateSuperToken list in the list which going to be returned
					classificationList.append(predicateSuperTokenList)

					# and initialize predicateSuperToken list
					predicateSuperTokenList = []

	# return categorized token list
	return classificationList


# define method to create file which is given in input to taggerTree programm
# listType specify what type of token arrives in input, description or predicate
def writeFileForTaggerTree (descPredList,typeList):

	# initialize a variable to know the indexing
	indexOfElement = 0

	# extrat length of predicate list
	lenPredList = len(descPredList)

	# for each element in list ( predicate or description )
	for element in descPredList:

		if typeList == "predicate":

			fileName = "inputFile_tagger/file_input_traggerTree_predicate.txt"

			# if it is the first predicate of the list
			if indexOfElement == 0:
				# have to open file in write mode
				openMode = 'w'
			else:
				# otherwise have to open file in append mode
				openMode = 'a'

			# open file in write mode
			with open(fileName,openMode) as file:

				# extrat length of token list
				lenList = len(element)

				# initialize a variable for index count token list
				index = 0

				# insert one token for each line
				for token in element:

					# check if is not the last token
					if index < lenList:

						# write token and "new line" character
						file.write(token+'\n')

					# increse index
					index = index+1
					
				# if it is the last token of the last predicate don't write the new line character
				if indexOfElement < lenPredList - 1 :
					file.write('.'+'\n')
				else:
					file.write('.')

					
			# increse index
			indexOfElement = indexOfElement + 1
		else:
			fileName = "inputFile_tagger/file_input_traggerTree_description.txt"

			# if it is the first predicate of the list
			if indexOfElement == 0:
				# have to open file in write mode
				openMode = 'w'
			else:
				# otherwise have to open file in append mode
				openMode = 'a'

			# open file in write mode
			with open(fileName,openMode) as file:

				# extrat length of list
				lenList = len(element["tokenizedDescription"])

				# initialize a variavle for index count
				index = 0

				# insert one token for each line
				for token in element["tokenizedDescription"]:

					# check if is not the last token
					if index < lenList:

						# write token and "new line" character
						file.write(token+'\n')

					# increse index
					index = index+1

				# if it is the last token of the last description don't write the new line character
				if indexOfElement < lenPredList :
					file.write('\n')

					
			# increse index
			indexOfElement = indexOfElement + 1


	return fileName



# define method to create a new file to solve the omitted accent mark problem
def rewriteFilePredicateTaggerTree (tokenList,inputFile):

	# open file in write mode
	with open(inputFile,'w') as file:

		# extrat length of list
		lenList = len(tokenList)

		# initialize a variavle for index count
		index = 0

		# insert one token for each line
		for token in tokenList:

			# check if is not the last token
			if index < lenList-1:

				# write token and "new line" character
				file.write(token+'\n')
			else:
				# otherwise dont write new line
				file.write(token+'\n.')

			# increse index
			index = index+1


# method to read csv file to test application
def readCTSV( fileName,splitChar='\t',encodingMode='utf-8' ):
	
	# open file in read mode
	with codecs.open(fileName, 'rb',encodingMode) as file:
	
	
		# create an istance of a csv reader
		reader = csv.reader(file,delimiter=splitChar,quoting=csv.QUOTE_MINIMAL)

		# initialize list in which predicate going to be saved
		predicateList = []

		# initialize list in which description going to be saved
		descriptionList = []

		# initialize list in which fail going to be saved
		failList = []

		# for each row read from file
		for row in reader:
			try:
				
				# create an istance of predicate class with name and type extracted from row
				newPredicate = predicate( row[0],row[1] )

				# extract test tagged description
				description = {'testTaggedDescription':row[2]}

				# extract description wrote in natural lenguage
				description['naturalDescription'] = row[3].replace("_"," ").replace("d'","di ")

				# save refered predicate in the description list
				description['predicate'] = newPredicate

				# append new predicate in predicate list
				predicateList.append(newPredicate)
				# append new description in description list
				descriptionList.append(description)

			# in case of IndexError
			except IndexError as exception:
				# save row in failList
				failList.append(row)

	# return list of result
	return [descriptionList,predicateList,failList]

# method to read csv or tsv for one of description and predicate list
def readOneListCTSV( fileName,typeRead,splitChar='\t',encodingMode='utf-8' ):
	
	# open file in read mode
	with codecs.open(fileName, 'rb',encodingMode) as file:
	
	
		# create an istance of a csv reader
		reader = csv.reader(file,delimiter=splitChar,quoting=csv.QUOTE_MINIMAL)

		# initialize list in which results going to be saved
		resultList = []

		# initialize list in which fail going to be saved
		failList = []

		# check what it is going to be read, if a predicate
		if typeRead == "predicate":

			# for each row read from file
			for row in reader:
				try:

					# create an istance of predicate class with name and type extracted from row
					newPredicate = predicate( row[0],row[1] )
					
					# append new description in description list
					resultList.append(newPredicate)

				# in case of IndexError
				except IndexError as exception:
					# save row in failList
					failList.append(row)

		else:
			# otherwise it is a description

			# for each row read from file
			for row in reader:
				try:

					# extract description wrote in natural lenguage
					description = {'naturalDescription':row[0]}

					# append new description in description list
					resultList.append(description)

				# in case of IndexError
				except IndexError as exception:
					# save row in failList
					failList.append(row)

	# return list of result
	return [resultList,failList]


# define method to read owl/xml file
def readOWLXML( filePath ):

	# initialize variable that going to be returned
	predicateList = []

	# extract ontology from file
	ontologyInformation = get_ontology(filePath).load()

	# extract classes from ontology given
	conceptList = ontologyInformation.classes()
	if conceptList != None:

		# insert concept list in predicate one
		for concept in conceptList:
			# create an istance of predicate class with name and type
			newPredicate = predicate( concept.name , "concept" )

			# insert new predicate in list
			predicateList.append(newPredicate)

	# extract object properties from ontology given
	attributeList = ontologyInformation.object_properties()

	if attributeList != None:

		# insert concept list in predicate one
		for attribute in attributeList:
			# create an istance of predicate class with name and type
			newPredicate = predicate( attribute.name , "attribute" )

			# insert new predicate in list
			predicateList.append(newPredicate)

	# extract data properties from ontology given
	roleList = ontologyInformation.data_properties()

	if roleList != None:

		# insert concept list in predicate one
		for role in roleList:
			# create an istance of predicate class with name and type
			newPredicate = predicate( role.name , "role" )

			# insert new predicate in list
			predicateList.append(newPredicate)




	# READ ALSO DESCRIPTION
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#




	# return predicate list
	return predicateList


# define method to read configuration file
# configuration file is organized in this way:

# PREDICATE CHANGE MAPPING								possible change to do in predicate list
# currentForm->changeForm								example:	est->è
# 														new line \n
# STOP WORD												stop word list
# det 													grammatical group to not check
# pro
# 														new line \n
# PREDICATE INPUT FILE											( tsv or owl/xml ) input file to programm 
# tsv
#
# DESCRIPTION INPUT FILE											( tsv or owl/xml ) input file to programm 
# tsv
#
# DELIMITER 											( _ or - or upper ) delimiter char for predicate , if word in predicate are delimited with an upper char, write upper
# _

def readConfig(fileName):

	# define name of section in file config
	mapTitle = "PREDICATE CHANGE MAPPING\n"

	stopWordTitle = "STOP WORD\n"

	predicateInputTitle = "PREDICATE INPUT FILE\n"

	descriptionInputTitle = "DESCRIPTION INPUT FILE\n"

	delimitTitle = "DELIMITER\n"

	# create variable that going to be returned
	mapDictionary = {}

	stopWordList = []

	predicatInputType = ""

	descriptionInputType = ""

	delimiter = ""

	# open file
	with codecs.open(fileName,'r',encoding='utf-8') as file:

		# read all file and insert in a list
		configList = file.readlines()

		# extract length of the list
		lenList = len(configList)

		# check if there are some mapping changes
		if mapTitle in configList:

			# extract index of this line 
			mapIndex = configList.index(mapTitle)

			# initialize variable for the while
			index = mapIndex+1

			# variable for stopping while
			stopWhile = False

			# while untill stopWhile is false
			while not stopWhile:

				# if index is over the end of list stop loop
				if not index<lenList:
					stopWhile = True
				# if current line is a new line char stop loop
				else:
					if configList[index] == '\n':
						stopWhile = True
					# otherwise save parameter
					else:
						# extract line from list
						currentLine = configList[index]

						# if last char of param is a new line, delete it
						if currentLine[len(currentLine)-1] == '\n':
							# delete last character "new line" from line
							currentLine = currentLine[:-1]

						# extract line and split it with '->'
						splittedLine = currentLine.split('->')

						# save parameter of mapping
						mapDictionary = { splittedLine[0]:splittedLine[1] }

						# go on loop
						index = index + 1

		# check if there are some stop word
		if stopWordTitle in configList:

			# extract index of this line 
			stopWordIndex = configList.index(stopWordTitle)

			# initialize variable for the while
			index = stopWordIndex+1

			# variable for stopping while
			stopWhile = False

			# while untill stopWhile is false
			while not stopWhile:

				# if index is over the end of list stop loop
				if not index<lenList:
					stopWhile = True
				# if current line is a new line char stop loop
				elif configList[index] == '\n':
					stopWhile = True
				# otherwise save parameter
				else:

					# extract line from list
					currentLine = configList[index]

					# if last char of param is a new line, delete it
					if currentLine[len(currentLine)-1] == '\n':
						# delete last character "new line" from line
						currentLine = currentLine[:-1]

					stopWordList.append(currentLine)

					# go on loop
					index = index + 1

		# check if there are some info for predicate input file
		if predicateInputTitle in configList:

			# extract index of this line 
			inputIndex = configList.index(predicateInputTitle)

			# if next index is in list
			if inputIndex+1 < lenList:

				# extract line from list
				currentLine = configList[inputIndex+1]

				# if last char of param is a new line, delete it
				if currentLine[len(currentLine)-1] == '\n':
					# delete last character "new line" from line
					currentLine = currentLine[:-1]

				# extract and save parameter
				predicatInputType = currentLine

		# check if there are some info for description input file
		if descriptionInputTitle in configList:

			# extract index of this line 
			inputIndex = configList.index(descriptionInputTitle)

			# if next index is in list
			if inputIndex+1 < lenList:

				# extract line from list
				currentLine = configList[inputIndex+1]

				# if last char of param is a new line, delete it
				if currentLine[len(currentLine)-1] == '\n':
					# delete last character "new line" from line
					currentLine = currentLine[:-1]

				# extract and save parameter
				descriptionInputType = currentLine


		# check if there are some info for predicate delimiter
		if delimitTitle in configList:

			# extract index of this line 
			delimitIndex = configList.index(delimitTitle)

			# if next index is in list
			if delimitIndex+1 < lenList:

				# extract line from list
				currentLine = configList[delimitIndex+1]

				# if last char of param is a new line, delete it
				if currentLine[len(currentLine)-1] == '\n':
					# delete last character "new line" from line
					currentLine = currentLine[:-1]

				# extract and save parameter
				delimiter = currentLine


	# return all variable
	return [mapDictionary,stopWordList,predicatInputType,descriptionInputType,delimiter]




