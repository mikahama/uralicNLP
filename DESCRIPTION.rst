============
Uralic NLP
============

Uralic NLP is a Python library for processing small Uralic languages. The languages that are currently supported are Skolt Sami, Ingrian, Meadow & Eastern Mari, Votic, Olonets-Karelian, Erzya, Moksha, Hill Mari, Udmurt, Tundra Nenets, Komi-Permyak and Finnish.

Currently, this tool provides uralicApi functionality which uses the API of sanat.csc.fi. Over this API, it's possible to do **morphological analysis**, **morphological generation**, **lemmatization** and **dictionary search** for these languages.

This library provides **Omorfi as a service for Finnish**.

***************
Usage
***************
    ``from uralicNLP import uralicApi``

    ``print uralicApi.analyze("voita", "fin") #Morphological analysis for the Finnish word form voita``

    ``print uralicApi.generate("käsi+N+Sg+Par", "fin") #Generates the singular partitive form of the Finnish word käsi``

    ``print uralicApi.dictionary_search("car", "sms") #Does a dictionary search for the word car in the Skolt Sami dictionary``

    ``print uralicApi.lemmatize("voita", "fin") #Lists possible lemmas for the Finnish word form voita``

********************
Further information
********************

A proper documentation is available in the `Uralic NLP GitHub <https://github.com/mikahama/uralicNLP>`_
.

You might also be interested in `using Korp on Python <https://mikalikes.men/korp-and-python-access-corpora-from-your-python-code/>`_ to access corpora of Uralic languages.

This library will have more functionality in the future as my PhD studies progress. This library and the API was created by `Mika Hämäläinen <https://mikakalevi.com>`_
.