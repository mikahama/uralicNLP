# Uralic NLP
Uralic NLP is a natural language processing library for small Uralic languages. Currently its functionality is provided by sanat.csc.fi API which is also developed by [Mika Hämäläinen](https://mikakalevi.com).

Uralic NLP can produce **morphological analysis**, **generate morphological forms**, **lemmatize words** and **give lexical information** about words in Uralic languages. At the time of writing, the following languages are supported: Skolt Sami, Ingrian, Meadow & Eastern Mari, Votic, Olonets-Karelian, Erzya, Moksha, Hill Mari, Udmurt, Tundra Nenets, Komi-Permyak and Finnish. This information originates from FST tools and dictionaries developed in the [Giellatekno infrastructure](http://giellatekno.uit.no/).

## Installation
The library can be installed from [PyPi](https://pypi.python.org/pypi/uralicNLP/).

    pip install uralicNLP

## Usage

### List supported languages
The API is under constant development and new languages will be added to the Sanat infrastructure. That's why Uralic NLP provides a functionality for looking up the list of currently supported languages. The method returns 3 letter ISO codes for the languages.

    >>from uralicNLP import uralicApi
    >>uralicApi.supported_languages()
    {'languages': ['sms', 'izh', 'mhr', 'vot', 'olo', 'myv', 'mdf', 'mrj', 'udm', 'yrk', 'koi', 'fin']}
  
### Lemmatize words
A word form can be lemmatized with Uralic NLP. This does not do any disambiguation but rather returns a list of all the possible lemmas.

    >>from uralicNLP import uralicApi
    >>uralicApi.lemmatize("вирев", "myv")
    {'results': ['вирев', 'вирь']}
  
  An example of lemmatizing the word *вирев* in Erzya (myv).

### Morphological analysis
Apart from just getting the lemmas, it's also possible to perform a complete morphological analysis.

    >>from uralicNLP import uralicApi
    >>uralicApi.analyze("voita", "fin")
    {'query': 'voita', 'language': 'fin', 'analysis': [['voi+N+Sg+Par', 0.0], ['voi+N+Pl+Par', 0.0], ['voitaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voitaa+V+Act+Imprt+Sg2', 0.0], ['voitaa+V+Act+Ind+Prs+ConNeg', 0.0], ['voittaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voittaa+V+Act+Imprt+Sg2', 0.0], ['voittaa+V+Act+Ind+Prs+ConNeg', 0.0], ['vuo+N+Pl+Par', 0.0]]}
  
An example of analyzing the word *voita* in Finnish (fin).

### Morphological generation
From a lemma and a morphological analysis, it's possible to generate the desired word form. 


    >>from uralicNLP import uralicApi
    >>uralicApi.generate("käsi+N+Sg+Par", "fin")
    {'query': 'käsi+N+Sg+Par', 'language': 'fin', 'analysis': [['kättä', 0.0]]}
  
An example of generating the singular partitive form for the Finnish noun *käsi*. The result is *kättä*.

### Lexical information
Uralic NLP makes it possible to obtain the information available in sanat.csc.fi entries in JSON format. The information can contain data such as translations, example sentences, semantic tags, morphological information and so on. You have to define the language code of the dictionary. 

For example, "sms" selects the Skolt Sami dictionary. However, the word used to query can appear in any language. If the word is a lemma in Skolt Sami, the result will appear in "exact_match", if it's a word form for a Skolt Sami word, the results will appear in "lemmatized", and if it's a word in some other language, the results will appear in "other\_languages" under the language code of that language. I.e if you search for *cat* in the Skolt Sami dictionary, you will get a result of a form {"other\_languages": "eng": [Skolt Sami lexical items that translate to cat]}



    >>from uralicNLP import uralicApi
    >>uralicApi.dictionary_search("car", "sms")
    {'lemmatized': [], 'query': 'car', 'exact_match': {}, 'other_languages': {'eng': [{'lemma': 'autt', ...}]}, 'language': 'sms'}
  
An example of querying the Skolt Sami dictionary with *car*.
