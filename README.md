# NLP-ontology-description-wiki
Support tool which automatically insert necessary wiki tag in description of predicate based on an ontology dictionary.


For the usage, download the repository. Download TaaggerTree program from http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/. Download the Owlready2-0.4 if you need to read ontology from .owl file.
 Then include all the project in your .py file and call the function core() whit this input:
 - config file;
 - input file predicate;
 - input file description;
 - predicate delimiter;
 - stopWordList;
 - accentProblem True if there is not accent mark in predicate.

It is possible to choose some configuration information as:
- If there are some trick solution in predicate list, example write "est" instead of "è" for some implementation reason it is possible 
to specify it in configuration file in the form est->è , so the core() will change it;
- Have to specify the predicate file name in input;
- Have to specify the description name file in input, but it is possible to pass a single description as input in main method;
- Have to specify which character delimite the predicate words.

See core.py for more information.
