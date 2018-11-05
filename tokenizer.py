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

from nltk import word_tokenize , regexp_tokenize


# definisco la funzione per a tokenizzazione delle descrizioni
def tokenizeDescription (descrizione):
	#dichiaro i pattern che saranno utilizzati per la tokenizzazione, cioe quelli riconosciuti come "token"
	# - (?:[A-Za-z]\.)+ tutti gli acronimi puntati es. U.S.A. o S.p.a. -> _U.S.A._ 		_S.p.a._
	# - [a-z]+(?:-[a-z]+) tutte le parole divise da un trattino saranno lasciate unite sotto un unico token es. semi-automatico -> _semi-automatico_
	# -	\w+(?:\')* tutte le parole troncate con l'apostrofo saranno considerati con l'apostrofo es. l'ultima -> _l'_	_ultima_
	# - \$?\d+(?:\.\d)?%? tutte i numeri che fanno riferimento a prezzi, percentuali o simili saranno intesi come unico token es. $12.22 o 18% -> _$12.22_	_18%_
	# - [\[\].,;\"'?!(){}\-:_/] qualsiasi carattere di punteggiatura ( tranne l'apostrofo, vedi sopra ) sara considerato come token a se stante
	patternDescrizione = r"(?:[A-Za-z]\.)+|[a-z]+(?:-[a-z]+)|\w+(?:\')*|\$?\d+(?:\.\d)?%?|[\[\].,;\"'?!(){}\-:/]"
	
	# tokenizzo la descrizione in base al pattern definitio precedentemente
	descrizione = regexp_tokenize(descrizione,patternDescrizione)

	



	return descrizione

# definisco la funzione per a tokenizzazione delle descrizioni
def tokenizeTestDescription (descrizione):
	#dichiaro i pattern che saranno utilizzati per la tokenizzazione, cioe quelli riconosciuti come "token"
	# - (?:[A-Za-z]\.)+ tutti gli acronimi puntati es. U.S.A. o S.p.a. -> _U.S.A._ 		_S.p.a._
	# - [a-z]+(?:-[a-z]+) tutte le parole divise da un trattino saranno lasciate unite sotto un unico token es. semi-automatico -> _semi-automatico_
	# -	\w+(?:\')* tutte le parole troncate con l'apostrofo saranno considerati con l'apostrofo es. l'ultima -> _l'_	_ultima_
	# - \$?\d+(?:\.\d)?%? tutte i numeri che fanno riferimento a prezzi, percentuali o simili saranno intesi come unico token es. $12.22 o 18% -> _$12.22_	_18%_
	# - [\[\].,;\"'?!(){}\-:_/] qualsiasi carattere di punteggiatura ( tranne l'apostrofo, vedi sopra ) sara considerato come token a se stante
	patternDescrizione = r"(?:[A-Za-z]\.)+|[a-z]+(?:-[a-z]+)|\w+(?:\')*|\$?\d+(?:\.\d)?%?|[\[\].,;\"'?\|!(){}\-:_/]"

	
	# tokenizzo la descrizione in base al pattern definitio precedentemente
	descrizione = regexp_tokenize(descrizione,patternDescrizione)


	return descrizione



# definisco la funzione per la tokenizzazine dei predicati ontologici sapendo che sono separati da un underscore
def tokenizePredicate ( listaPredicati,delimiterChar=None ):

	tokenizedPredicate = []

	# check if delimiter character is None
	if delimiterChar == None:

		# per ogni predicato all'interno della lista
		for predicato in listaPredicati:

			tokenList = []

			# tokenizzo il predicato splittando semplicemente
			predicateName = predicato.getName()

			predicateName = predicateName.replace('_',' ')

			totalLen = len(predicateName)

			newPredicate = predicateName

			changeNumber = 0

			# indice
			charIndex = 1

			# per ogni carattere del predicato
			while charIndex < totalLen+changeNumber-1:

				lettera = newPredicate[charIndex]

				# controllo se è maiuscola
				if lettera.isupper() and not newPredicate[charIndex+1].isupper():

					# in tal caso aggiungo al nuovo predicato uno spazio
					newPredicate = newPredicate[:charIndex]+" "+lettera.lower()+newPredicate[charIndex+1:]

					changeNumber = changeNumber + 1

				charIndex = charIndex + 1

			tokenList = newPredicate.split(' ')

			# salvo il risultato nella lista ricevuta in input
			tokenizedPredicate.append(tokenList)

	elif delimiterChar == "upper":

		# per ogni predicato all'interno della lista
		for predicato in listaPredicati:

			tokenList = []

			# tokenizzo il predicato splittando semplicemente
			predicateName = predicato.getName()

			totalLen = len(predicateName)

			newPredicate = predicateName

			changeNumber = 0

			# indice
			charIndex = 1

			# per ogni carattere del predicato
			while charIndex < totalLen+changeNumber-1:

				lettera = newPredicate[charIndex]

				# controllo se è maiuscola
				if lettera.isupper() and not newPredicate[charIndex+1].isupper():

					# in tal caso aggiungo al nuovo predicato uno spazio
					newPredicate = newPredicate[:charIndex]+" "+lettera.lower()+newPredicate[charIndex+1:]

					changeNumber = changeNumber + 1

				charIndex = charIndex + 1

			tokenList = newPredicate.split(' ')

			# salvo il risultato nella lista ricevuta in input
			tokenizedPredicate.append(tokenList)

	else:

		# per ogni predicato all'interno della lista
		for predicato in listaPredicati:
				
			# tokenizzo il predicato splittando semplicemente
			tokenList = predicato.getName().split(delimiterChar)

			# salvo il risultato nella lista ricevuta in input
			tokenizedPredicate.append(tokenList)

	return tokenizedPredicate