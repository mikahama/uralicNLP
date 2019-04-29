# UralicNLP

[![Build Status](https://travis-ci.com/mikahama/uralicNLP.svg?branch=master)](https://travis-ci.com/mikahama/uralicNLP) [![Updates](https://pyup.io/repos/github/mikahama/uralicNLP/shield.svg)](https://pyup.io/repos/github/mikahama/uralicNLP/)

UralicNLP is a natural language processing library for small Uralic languages. Currently its functionality is provided by [akusanat.com](https://akusanat.com) API which is also developed by [Mika Hämäläinen](https://mikakalevi.com).

UralicNLP can produce **morphological analysis**, **generate morphological forms**, **lemmatize words** and **give lexical information** about words in Uralic languages. At the time of writing, the following languages are supported: Skolt Sami, Ingrian, Meadow & Eastern Mari, Votic, Olonets-Karelian, Erzya, Moksha, Hill Mari, Udmurt, Tundra Nenets, Komi-Permyak and Finnish. This information originates from FST tools and dictionaries developed in the [Giellatekno infrastructure](https://victorio.uit.no/langtech/trunk/). Currently, UralicNLP uses the nightly builds for languages supported by Apertium and less frequently updated FSTs and CGs for the other languages.

## Installation
The library can be installed from [PyPi](https://pypi.python.org/pypi/uralicNLP/).

    pip install uralicNLP
   
In case you want to use the Constraint Grammar features (*from uralicNLP.cg3 import Cg3*), you will also need to [install VISL CG-3](https://mikalikes.men/how-to-install-visl-cg3-on-mac-windows-and-linux/).

If you are using Linux and you run into problems with installing hfst dependency, you can find some help on [a blog post on installing hfst](https://mikalikes.men/using-hfst-on-python/)

## Usage

### List supported languages
The API is under constant development and new languages will be added to the Sanat infrastructure. That's why UralicNLP provides a functionality for looking up the list of currently supported languages. The method returns 3 letter ISO codes for the languages.

    from uralicNLP import uralicApi
    uralicApi.supported_languages()
    >>{u'languages': [u'sms', u'izh', u'mhr', u'vot', u'olo', u'myv', u'mdf', u'mrj', u'udm', u'yrk', u'koi', u'kpv', u'fin'], u'morph': [u'mdf', u'mhr', u'sma', u'olo', u'rus', u'mrj', u'nob', u'fin', u'sms', u'cor', u'deu', u'kpv', u'lav', u'liv', u'kal', u'udm', u'nds', u'est', u'fao', u'izh', u'vot', u'smj', u'smn', u'sme', u'lut', u'vro', u'yrk', u'myv', u'gle', u'crk', u'koi']}

The *languages* key lists the languages that are supported by the lexical lookup, whereas *morph* lists the languages that have morphological FSTs and optionally CGs.

### Download the models 

If you have a lot of data to process, it might be a good idea to download the morphological models to your computer locally. This can be done easily.

    from uralicNLP import uralicApi
    uralicApi.download("fin")

When models are installed, *generate()*, *analyze()* and *lemmatize()* methods will automatically use them instead of the server side API. [More information about the models](https://github.com/mikahama/uralicNLP/wiki/Models).

Use **uralicApi.model_info(language)** to see information about the FSTs and CGs such as license and authors. If you know how to make this information more accurate, please don't hesitate to open an issue on GitHub

    from uralicNLP import uralicApi
    uralicApi.model_info("fin")


### Lemmatize words
A word form can be lemmatized with UralicNLP. This does not do any disambiguation but rather returns a list of all the possible lemmas.

    from uralicNLP import uralicApi
    uralicApi.lemmatize("вирев", "myv")
    >>['вирев', 'вирь']
  
An example of lemmatizing the word *вирев* in Erzya (myv). By default, a **descriptive** analyzer is used. Use *uralicApi.lemmatize("вирев", "myv", descrpitive=False)*.

### Morphological analysis
Apart from just getting the lemmas, it's also possible to perform a complete morphological analysis.

    from uralicNLP import uralicApi
    uralicApi.analyze("voita", "fin")
    >>[['voi+N+Sg+Par', 0.0], ['voi+N+Pl+Par', 0.0], ['voitaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voitaa+V+Act+Imprt+Sg2', 0.0], ['voitaa+V+Act+Ind+Prs+ConNeg', 0.0], ['voittaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voittaa+V+Act+Imprt+Sg2', 0.0], ['voittaa+V+Act+Ind+Prs+ConNeg', 0.0], ['vuo+N+Pl+Par', 0.0]]
  
An example of analyzing the word *voita* in Finnish (fin). The default analyzer is **descriptive**. To use a normative analyzer instead, use *uralicApi.analyze("voita", "fin", descrpitive=False)*

### Morphological generation
From a lemma and a morphological analysis, it's possible to generate the desired word form. 

    from uralicNLP import uralicApi
    uralicApi.generate("käsi+N+Sg+Par", "fin")
    >>[['kättä', 0.0]]
  
An example of generating the singular partitive form for the Finnish noun *käsi*. The result is *kättä*. The default generator is a **normative dictionary** generator. *uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False)* uses a regular normative generator and *uralicApi.generate("käsi+N+Sg+Par", "fin", descrpitive=True)* a descriptive generator.


### Access the HFST transducer

If you need to get a lower level access to [the HFST transducer object](https://hfst.github.io/python/3.12.1/classhfst_1_1HfstTransducer.html), you can use th following code

    from uralicNLP import uralicApi
    sms_generator = uralicApi.get_transducer("sms", analyzer=False) #generator
    sms_analyzer = uralicApi.get_transducer("sms", analyzer=True) #analyzer

The same parameters can be used here as for *generate()* and *analyze()* to specify whether you want to use the normative or descriptive analyzers and so on. The defaults are *get_transducer(language, cache=True, analyzer=True, descrpitive=True, dictionary_forms=True)*.

### Syntax - Constraint Grammar disambiguation

**Note** this requires the models to be installed (see above) and [VISL CG-3](https://mikalikes.men/how-to-install-visl-cg3-on-mac-windows-and-linux/). The disambiguation process is easy.

    from uralicNLP.cg3 import Cg3
    sentence = "Kissa voi nauraa"
    tokens = sentence.split(" ") #Do a simple tokenization for the sentence
    cg = Cg3("fin")
    print cg.disambiguate(tokens)
    >>[(u'Kissa', [<Kissa - N, Prop, Sg, Nom, <W:0.000000>>, <kissa - N, Sg, Nom, <W:0.000000>>]), (u'voi', [<voida - V, Act, Ind, Prs, Sg3, <W:0.000000>>]), (u'nauraa', [<nauraa - V, Act, InfA, Sg, Lat, <W:0.000000>>])]
    
The return object is a list of tuples. The first item in each tuple is the word form used in the sentence, the second item is a list of *Cg3Word* objects. In the case of a full disambiguation, these lists have only one Cg3Word object, but some times the result of the disambiguation still has some ambiguity. Each Cg3Word object has three variables *lemma*, *form* and *morphology*.

    disambiguations = cg.disambiguate(tokens)
    for disambiguation in disambiguations:
        possible_words = disambiguation[1]
        for possible_word in possible_words:
            print possible_word.lemma, possible_word.morphology
    >>Kissa [u'N', u'Prop', u'Sg', u'Nom', u'<W:0.000000>']
    >>kissa [u'N', u'Sg', u'Nom', u'<W:0.000000>']
    >>voida [u'V', u'Act', u'Ind', u'Prs', u'Sg3', u'<W:0.000000>']
    >>nauraa [u'V', u'Act', u'InfA', u'Sg', u'Lat', u'<W:0.000000>']
    
The *cg.disambiguate* takes in *remove_symbols* as an optional argument. Its default value is *True* which means that it removes the symbols (segments surrounded by @) from the FST output before feeding it to the CG disambiguator. If the value is set to *False*, the FST morphology is fed in to the CG unmodified.

The **default FST analyzer is a descriptive one**, to use a normative analyzer, set the *descriptive* parameter to False *cg.disambiguate(tokens,descrpitive=False)*.

### Lexical information
UralicNLP makes it possible to obtain the information available in sanat.csc.fi entries in JSON format. The information can contain data such as translations, example sentences, semantic tags, morphological information and so on. You have to define the language code of the dictionary. 

For example, "sms" selects the Skolt Sami dictionary. However, the word used to query can appear in any language. If the word is a lemma in Skolt Sami, the result will appear in "exact_match", if it's a word form for a Skolt Sami word, the results will appear in "lemmatized", and if it's a word in some other language, the results will appear in "other\_languages" under the language code of that language. I.e if you search for *cat* in the Skolt Sami dictionary, you will get a result of a form {"other\_languages": "eng": [Skolt Sami lexical items that translate to cat]}


    from uralicNLP import uralicApi
    uralicApi.dictionary_search("car", "sms")
    >>{'lemmatized': [], 'query': 'car', 'exact_match': {}, 'other_languages': {'eng': [{'lemma': 'autt', ...}]}, 'language': 'sms'}
  
An example of querying the Skolt Sami dictionary with *car*.

### Parsing UD CoNLL-U annotated TreeBank data

UralicNLP comes with tools for parsing and searching CoNLL-U formatted data. Please refer to [the Wiki for the UD parser documentation](https://github.com/mikahama/uralicNLP/wiki/UD-parser).

### Semantics

UralicNLP provides semantic models for Finnish (SemFi) and other Uralic languages (SemUr) for Komi-Zyrian, Erzya, Moksha and Skolt Sami. [Find out how to use semantic models](https://github.com/mikahama/uralicNLP/wiki/Semantics-(SemFi,-SemUr))

### Other functionalities

- [Machine Translation](https://github.com/mikahama/uralicNLP/wiki/Machine-Translation)
- [Finnish Dependency Parsing](https://github.com/mikahama/uralicNLP/wiki/Dependency-parsing)

# Cite

If you use UralicNLP in an academic publication, please cite it as follows:

Mika Hämäläinen. (2018, January 9). UralicNLP (Version v1.0). Zenodo. http://doi.org/10.5281/zenodo.1143638

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1143638.svg)](https://doi.org/10.5281/zenodo.1143638)

For the FSTs and CGs, refer to the Giellatekno repository or use **uralicApi.model_info(language)**.

