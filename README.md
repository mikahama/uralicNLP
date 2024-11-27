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

## Large language models (LLMs)

UralicNLP supports a wide range of LLMs and it can even embed text in some endangered languages [Check out LLMs](https://github.com/mikahama/uralicNLP/wiki/Large-Language-Models).

UralicNLP can cluster texts into semantically similar categories. [Learn more about clustering](https://github.com/mikahama/uralicNLP/wiki/Semantics).

## List supported languages
The API is under constant development and new languages will be added to the nightly builds system. That's why UralicNLP provides a functionality for looking up the list of currently supported languages. The method returns 3 letter ISO codes for the languages.

    from uralicNLP import uralicApi
    uralicApi.supported_languages()
    >>{'cg': ['vot', 'lav', 'izh', 'rus', 'lut', 'fao', 'est', 'nob', 'ron', 'olo', 'bxr', 'hun', 'crk', 'chr', 'vep', 'deu', 'mrj', 'gle', 'sjd', 'nio', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'bak', 'kca', 'otw', 'ciw', 'fkv', 'nds', 'kpv', 'sme', 'sje', 'evn', 'oji', 'ipk', 'fit', 'fin', 'mns', 'rmf', 'liv', 'cor', 'mdf', 'yrk', 'tat', 'smj'], 'dictionary': ['vot', 'lav', 'rus', 'est', 'nob', 'ron', 'olo', 'hun', 'koi', 'chr', 'deu', 'mrj', 'sjd', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'fkv', 'mhr', 'kpv', 'sme', 'sje', 'hdn', 'fin', 'mns', 'mdf', 'vro', 'udm', 'smj'], 'morph': ['vot', 'lav', 'izh', 'rus', 'lut', 'fao', 'est', 'nob', 'swe', 'ron', 'eng', 'olo', 'bxr', 'hun', 'koi', 'crk', 'chr', 'vep', 'deu', 'mrj', 'ara', 'gle', 'sjd', 'nio', 'myv', 'som', 'sma', 'sms', 'smn', 'kal', 'bak', 'kca', 'otw', 'ciw', 'fkv', 'nds', 'mhr', 'kpv', 'sme', 'sje', 'evn', 'oji', 'ipk', 'fit', 'fin', 'mns', 'rmf', 'liv', 'cor', 'mdf', 'yrk', 'vro', 'udm', 'tat', 'smj']}

The *dictionary* key lists the languages that are supported by the lexical lookup, whereas *morph* lists the languages that have morphological FSTs and *cg* lists the languages that have a CG.

## Download models 

On the command line:

    python -m uralicNLP.download --languages fin eng

From python code:

    from uralicNLP import uralicApi
    uralicApi.download("fin")

When models are installed, *generate()*, *analyze()* and *lemmatize()* methods will automatically use them instead of the server side API. [More information about the models](https://github.com/mikahama/uralicNLP/wiki/Models).

## Lemmatize words
A word form can be lemmatized with UralicNLP. This does not do any disambiguation but rather returns a list of all the possible lemmas.

    from uralicNLP import uralicApi
    uralicApi.lemmatize("вирев", "myv")
    >>['вирев', 'вирь']
    uralicApi.lemmatize("luutapiiri", "fin", word_boundaries=True)
    >>['luuta|piiri', 'luu|tapiiri']
  
An example of lemmatizing the word *вирев* in Erzya (myv). By default, a **descriptive** analyzer is used. Use *uralicApi.lemmatize("вирев", "myv", descriptive=False)* for a non-descriptive analyzer. If *word_boundaries* is set to True, the lemmatizer will mark word boundaries with a |.

## Morphological analysis
Apart from just getting the lemmas, it's also possible to perform a complete morphological analysis.

    from uralicNLP import uralicApi
    uralicApi.analyze("voita", "fin")
    >>[['voi+N+Sg+Par', 0.0], ['voi+N+Pl+Par', 0.0], ['voitaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voitaa+V+Act+Imprt+Sg2', 0.0], ['voitaa+V+Act+Ind+Prs+ConNeg', 0.0], ['voittaa+V+Act+Imprt+Prs+ConNeg+Sg2', 0.0], ['voittaa+V+Act+Imprt+Sg2', 0.0], ['voittaa+V+Act+Ind+Prs+ConNeg', 0.0], ['vuo+N+Pl+Par', 0.0]]
  
An example of analyzing the word *voita* in Finnish (fin). The default analyzer is **descriptive**. To use a normative analyzer instead, use *uralicApi.analyze("voita", "fin", descriptive=False)*.

## Morphological generation
From a lemma and a morphological analysis, it's possible to generate the desired word form. 

    from uralicNLP import uralicApi
    uralicApi.generate("käsi+N+Sg+Par", "fin")
    >>[['kättä', 0.0]]
  
An example of generating the singular partitive form for the Finnish noun *käsi*. The result is *kättä*. The default generator is a **regular normative** generator. *uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=True)* uses a normative dictionary generator and *uralicApi.generate("käsi+N+Sg+Par", "fin", descriptive=True)* a descriptive generator.

## Morphological segmentation
UralicNLP makes it possible to split a word form into morphemes. (Note: this does not work with all languages)

    from uralicNLP import uralicApi
    uralicApi.segment("luutapiirinikin", "fin")
    >>[['luu', 'tapiiri', 'ni', 'kin'], ['luuta', 'piiri', 'ni', 'kin']]

In the example, the word _luutapiirinikin_ has two possible interpretations luu|tapiiri and luuta|piiri, the segmentation is done for both interpretations.

## Disambiguation

This section has been moved to [UralicNLP wiki page on disambiguation](https://github.com/mikahama/uralicNLP/wiki/Disambiguation).

## Dictionaries

Learn more about dictionaries in [the wiki page on dictionaries](https://github.com/mikahama/uralicNLP/wiki/Dictionaries).

## Parsing UD CoNLL-U annotated TreeBank data

UralicNLP comes with tools for parsing and searching CoNLL-U formatted data. Please refer to [the Wiki for the UD parser documentation](https://github.com/mikahama/uralicNLP/wiki/UD-parser).


## Other functionalities

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

