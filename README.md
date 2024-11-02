<h1 align="center">UralicNLP</h1>
<p align="center">Natural language processing for many languages</p>

[![Updates](https://pyup.io/repos/github/mikahama/uralicNLP/shield.svg)](https://pyup.io/repos/github/mikahama/uralicNLP/)  [![Downloads](https://static.pepy.tech/badge/uralicnlp)](https://pepy.tech/project/uralicnlp) [![DOI](https://joss.theoj.org/papers/10.21105/joss.01345/status.svg)](https://doi.org/10.21105/joss.01345)


UralicNLP can produce **morphological analyses**, **generate morphological forms**, **lemmatize words** and **give lexical information** about words in Uralic and other languages. The languages we support include the following languages: Finnish, Russian, German, English, Norwegian, Swedish, Arabic, Ingrian, Meadow & Eastern Mari, Votic, Olonets-Karelian, Erzya, Moksha, Hill Mari, Udmurt, Tundra Nenets, Komi-Permyak, North Sami, South Sami and Skolt Sami. Currently, UralicNLP uses stable builds for the supported languages. 

[See the catalog of supported languages](http://models.uralicnlp.com/nightly/)

Some of the supported languages: 🇸🇦 🇪🇸 🇮🇹 🇵🇹 🇩🇪 🇫🇷 🇳🇱 🇬🇧 🇷🇺 🇫🇮 🇸🇪 🇳🇴 🇩🇰 🇱🇻 🇪🇪

Check out [**UralicGUI** - a graphical user interface for UralicNLP](https://github.com/mikahama/uralicGUI).

☕ Check out UralicNLP [official Java version](https://github.com/mikahama/uralicNLP-Java)

♯ Check out UralicNLP [official C# version](https://github.com/mikahama/uralicNLP.net)

## Installation
The library can be installed from [PyPi](https://pypi.python.org/pypi/uralicNLP/).

    pip install uralicNLP
   
If you want to use the Constraint Grammar features (*from uralicNLP.cg3 import Cg3*), you will also need to install VISL CG-3.

**🆕 [Pyhfst](https://github.com/Rootroo-ltd/pyhfst)** UralicNLP uses a pure Python implementation of HFST!

### Faster analysis and generation

UralicNLP uses Pyhfst, which can also be installed with Cython support for faster processing times:

    pip install cython
    pip install --upgrade --force-reinstall pyhfst --no-cache-dir

## Usage

### [Check out LLMs](https://github.com/mikahama/uralicNLP/wiki/Large-Language-Models)

### List supported languages
The API is under constant development and new languages will be added to the nightly builds system. That's why UralicNLP provides a functionality for looking up the list of currently supported languages. The method returns 3 letter ISO codes for the languages.

    from uralicNLP import uralicApi
    uralicApi.supported_languages()
    >>{'cg': ['vot', 'lav', 'izh', 'rus', 'lut', 'fao', 'est', 'nob', 'ron', 'olo', 'bxr', 'hun', 'crk', 'chr', 'vep', 'deu', 'mrj', 'gle', 'sjd', 'nio', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'bak', 'kca', 'otw', 'ciw', 'fkv', 'nds', 'kpv', 'sme', 'sje', 'evn', 'oji', 'ipk', 'fit', 'fin', 'mns', 'rmf', 'liv', 'cor', 'mdf', 'yrk', 'tat', 'smj'], 'dictionary': ['vot', 'lav', 'rus', 'est', 'nob', 'ron', 'olo', 'hun', 'koi', 'chr', 'deu', 'mrj', 'sjd', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'fkv', 'mhr', 'kpv', 'sme', 'sje', 'hdn', 'fin', 'mns', 'mdf', 'vro', 'udm', 'smj'], 'morph': ['vot', 'lav', 'izh', 'rus', 'lut', 'fao', 'est', 'nob', 'swe', 'ron', 'eng', 'olo', 'bxr', 'hun', 'koi', 'crk', 'chr', 'vep', 'deu', 'mrj', 'ara', 'gle', 'sjd', 'nio', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'bak', 'kca', 'otw', 'ciw', 'fkv', 'nds', 'mhr', 'kpv', 'sme', 'sje', 'evn', 'oji', 'ipk', 'fit', 'fin', 'mns', 'rmf', 'liv', 'cor', 'mdf', 'yrk', 'vro', 'udm', 'tat', 'smj']}

The *dictionary* key lists the languages that are supported by the lexical lookup, whereas *morph* lists the languages that have morphological FSTs and *cg* lists the languages that have a CG.

### Download models 

If you have a lot of data to process, it might be a good idea to download the morphological models for use on your computer locally. This can be done easily. Although, it is possible to use the transducers over Akusanat API by passing *force_local=False*.

On the command line:

    python -m uralicNLP.download --languages fin eng

From python code:

    from uralicNLP import uralicApi
    uralicApi.download("fin")

When models are installed, *generate()*, *analyze()* and *lemmatize()* methods will automatically use them instead of the server side API. [More information about the models](https://github.com/mikahama/uralicNLP/wiki/Models).

Use **uralicApi.model_info(language)** to see information about the FSTs and CGs such as license and authors. If you know how to make this information more accurate, please don't hesitate to open an issue on GitHub.

    from uralicNLP import uralicApi
    uralicApi.model_info("fin")

To remove the models of a language, run

    from uralicNLP import uralicApi
    uralicApi.uninstall("fin")

### Lemmatize words
A word form can be lemmatized with UralicNLP. This does not do any disambiguation but rather returns a list of all the possible lemmas.

    from uralicNLP import uralicApi
    uralicApi.lemmatize("вирев", "myv")
    >>['вирев', 'вирь']
    uralicApi.lemmatize("luutapiiri", "fin", word_boundaries=True)
    >>['luuta|piiri', 'luu|tapiiri']
  
An example of lemmatizing the word *вирев* in Erzya (myv). By default, a **descriptive** analyzer is used. Use *uralicApi.lemmatize("вирев", "myv", descriptive=False)* for a non-descriptive analyzer. If *word_boundaries* is set to True, the lemmatizer will mark word boundaries with a |. [You can also use your own transducer](https://github.com/mikahama/uralicNLP/wiki/Models#using-your-own-transducers)

### Morphological analysis
Apart from just getting the lemmas, it's also possible to perform a complete morphological analysis.

    from uralicNLP import uralicApi
    uralicApi.analyze("voita", "fin")
    >>[['voi+N+Sg+Par', 0.0], ['voi+N+Pl+Par', 0.0], ['voitaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voitaa+V+Act+Imprt+Sg2', 0.0], ['voitaa+V+Act+Ind+Prs+ConNeg', 0.0], ['voittaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voittaa+V+Act+Imprt+Sg2', 0.0], ['voittaa+V+Act+Ind+Prs+ConNeg', 0.0], ['vuo+N+Pl+Par', 0.0]]
  
An example of analyzing the word *voita* in Finnish (fin). The default analyzer is **descriptive**. To use a normative analyzer instead, use *uralicApi.analyze("voita", "fin", descriptive=False)*. [You can also use your own transducer](https://github.com/mikahama/uralicNLP/wiki/Models#using-your-own-transducers)

### Morphological generation
From a lemma and a morphological analysis, it's possible to generate the desired word form. 

    from uralicNLP import uralicApi
    uralicApi.generate("käsi+N+Sg+Par", "fin")
    >>[['kättä', 0.0]]
  
An example of generating the singular partitive form for the Finnish noun *käsi*. The result is *kättä*. The default generator is a **regular normative** generator. *uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=True)* uses a normative dictionary generator and *uralicApi.generate("käsi+N+Sg+Par", "fin", descriptive=True)* a descriptive generator. [You can also use your own transducer](https://github.com/mikahama/uralicNLP/wiki/Models#using-your-own-transducers)

### Morphological segmentation
UralicNLP makes it possible to split a word form into morphemes. (Note: this does not work with all languages)

    from uralicNLP import uralicApi
    uralicApi.segment("luutapiirinikin", "fin")
    >>[['luu', 'tapiiri', 'ni', 'kin'], ['luuta', 'piiri', 'ni', 'kin']]

In the example, the word _luutapiirinikin_ has two possible interpretations luu|tapiiri and luuta|piiri, the segmentation is done for both interpretations.

### Access the HFST transducer

If you need to get a lower level access to [the HFST transducer object](https://hfst.github.io/python/3.12.1/classhfst_1_1HfstTransducer.html), you can use the following code

    from uralicNLP import uralicApi
    sms_generator = uralicApi.get_transducer("sms", analyzer=False) #generator
    sms_analyzer = uralicApi.get_transducer("sms", analyzer=True) #analyzer

The same parameters can be used here as for *generate()* and *analyze()* to specify whether you want to use the normative or descriptive analyzers and so on. The defaults are *get_transducer(language, cache=True, analyzer=True, descriptive=True, dictionary_forms=True)*.

### Disambiguation

This section has been moved to [UralicNLP wiki](https://github.com/mikahama/uralicNLP/wiki/Disambiguation).

### Dictionaries
UralicNLP makes it possible to obtain the lexicographic information from the Giella dictionaries. The information can contain data such as translations, example sentences, semantic tags, morphological information and so on. You have to define the language code of the dictionary. 

For example, "sms" selects the Skolt Sami dictionary. The word used to query, however, can appear in any language. If the word is a lemma in Skolt Sami, the result will appear in "exact_match", if it's a word form for a Skolt Sami word, the results will appear in "lemmatized", and if it's a word in some other language, the results will appear in "other\_languages", i.e if you search for *cat* in the Skolt Sami dictionary, you will get a result of a form {"other\_languages": [Skolt Sami lexical items that translate to cat]}

An example of querying the Skolt Sami dictionary with *car*.


    from uralicNLP import uralicApi
    uralicApi.dictionary_search("car", "sms")
    >>{'lemmatized': [], 'exact_match': [], 'other_languages': [{'lemma': 'autt', ...}, ...]
  
It is possible to list all lemmas in the dictionary:

    from uralicNLP import uralicApi
    uralicApi.dictionary_lemmas("sms")
    >> ['autt', 'sokk' ...]

You can also group the lemmas by part-of-speech

    from uralicNLP import uralicApi
    uralicApi.dictionary_lemmas("sms",group_by_pos=True)
    >> {"N": ['autt', 'sokk' ...], "V":[...]}

To find translations in an endangered language dictionary to a certain language, you can run this script

     from uralicNLP import uralicApi   
     uralicApi.get_translation("piânnai", "sms", "fin")
     >> ['koira']

The example above searches for the word piânnai in Skolt Sami dictionary and returns the translations in Finnish.

#### Fast Dictionary Look-ups

By default, UralicNLP uses a TinyDB backend. This is easy as it does not require an external database server, but it can be extremely slow. For this reason, UralicNLP provides a [MongoDB backend](https://www.mongodb.com/download-center/community).

Make sure you have both **MongoDB and [pymongo](https://pypi.org/project/pymongo/) installed**.

First, you will need to download the dictionary and import it to MongoDB. The following example shows how to do it for Komi-Zyrian.

    from uralicNLP import uralicApi

    uralicApi.download("kpv") #Download the latest dictionary data
    uralicApi.import_dictionary_to_db("kpv") #Update the MongoDB with the new data

After the initial setup, you can use the dictionary queries, but you will need to specify the backend.

    from uralicNLP import uralicApi
    from uralicNLP.dictionary_backends import MongoDictionary
    uralicApi.dictionary_lemmas("sms",backend=MongoDictionary)
    uralicApi.dictionary_search("car", "sms",backend=MongoDictionary)

Now you can query the dictionaries fast.

### Parsing UD CoNLL-U annotated TreeBank data

UralicNLP comes with tools for parsing and searching CoNLL-U formatted data. Please refer to [the Wiki for the UD parser documentation](https://github.com/mikahama/uralicNLP/wiki/UD-parser).

### Semantics

UralicNLP provides semantic models for Finnish (SemFi) and other Uralic languages (SemUr) for Komi-Zyrian, Erzya, Moksha and Skolt Sami. [Find out how to use semantic models](https://github.com/mikahama/uralicNLP/wiki/Semantics-(SemFi,-SemUr))

### Other functionalities

- [Machine Translation](https://github.com/mikahama/uralicNLP/wiki/Machine-Translation)
- [Finnish Dependency Parsing](https://github.com/mikahama/uralicNLP/wiki/Dependency-parsing)
- [ISO code to language name](https://github.com/mikahama/uralicNLP/wiki/uralicNLP.string_processing#iso_to_name)
- [Tokenization](https://github.com/mikahama/uralicNLP/wiki/Tokenization)

# Cite

If you use UralicNLP in an academic publication, please cite it as follows:

Hämäläinen, Mika. (2019). UralicNLP: An NLP Library for Uralic Languages. Journal of open source software, 4(37), [1345]. https://doi.org/10.21105/joss.01345

    @article{uralicnlp_2019, 
        title={{UralicNLP}: An {NLP} Library for {U}ralic Languages},
        DOI={10.21105/joss.01345}, 
        journal={Journal of Open Source Software}, 
        author={Mika Hämäläinen}, 
        year={2019}, 
        volume={4},
        number={37},
        pages={1345}
    }

For citing the FSTs and CGs, see *uralicApi.model_info(language)*.

The FST and CG tools and dictionaries come mostly from the [GiellaLT repositories](https://github.com/giellalt) and [Apertium](https://github.com/apertium).

