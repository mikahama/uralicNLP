============
Uralic NLP
============

Uralic NLP is a Python library for processing small Uralic languages. The languages that are currently supported are Skolt Sami, Ingrian, Meadow & Eastern Mari, Votic, Olonets-Karelian, Erzya, Moksha, Hill Mari, Udmurt, Tundra Nenets, Komi-Permyak and Finnish...

Currently, this tool provides uralicApi functionality which uses the API of sanat.csc.fi. Over this API, it's possible to do **morphological analysis**, **morphological generation**, **lemmatization** and **dictionary search** for these languages. It is also possible to download the morphological models and constraint grammars to your computer for faster processing (see Further information for more).

This library provides **Omorfi as a service for Finnish**.

***************
Usage
***************
    ``from uralicNLP import uralicApi``

    ``print uralicApi.analyze("voita", "fin") #Morphological analysis for the Finnish word form voita``

    ``print uralicApi.generate("käsi+N+Sg+Par", "fin") #Generates the singular partitive form of the Finnish word käsi``

    ``print uralicApi.dictionary_search("car", "sms") #Does a dictionary search for the word car in the Skolt Sami dictionary``

    ``print uralicApi.lemmatize("voita", "fin") #Lists possible lemmas for the Finnish word form voita``
    
    ``from uralicNLP.cg3 import Cg3``

    ``uralicApi.download("fin") #Downloads the CG and morphological models for Finnish``

    ``cg = Cg3("fin") #Creates a constraint grammar (CG) disambiguator object for Finnish``

    ``cg.disambiguate(["Kissa","voi","nauraa", "!"]) #Uses the CG to disambiguate the words in a tokenized sentence``

********************
Further information
********************

A proper documentation is available in the `Uralic NLP GitHub <https://github.com/mikahama/uralicNLP>`_
.

You might also be interested in `using Korp on Python <https://mikalikes.men/korp-and-python-access-corpora-from-your-python-code/>`_ to access corpora of Uralic languages.

This library will have more functionality in the future as my PhD studies progress. This library and the API was created by `Mika Hämäläinen <https://mikakalevi.com>`_
.