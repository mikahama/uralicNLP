---
title: 'UralicNLP: An NLP Library for Uralic Languages'
tags:
  - Python
  - morphology
  - syntax
  - semantics
  - constraint grammar
  - finite state morphology
  - Uralic languages
  - natural language processing
  - endangered languages
authors:
  - name: Mika Hämäläinen
    orcid: 0000-0001-9315-1278
    affiliation: 1
affiliations:
 - name: Department of Digital Humanities, University of Helsinki
   index: 1
date: 3 March 2019
bibliography: paper.bib
---

# Introduction

In the past years the natural language processing (NLP) tools and resources for the small Uralic languages have received a major uplift. The open-source infrastructure by Giellatekno [@Trosterud] has served a key role in gathering these tools and resources in an open environment for researchers to use.

However, the many of the crucially important NLP tools, such as FSTs (finite-state transducers) [cf. @BeesleyKarttunen03] for processing morphology and CGs (constraint grammars) [cf. @karlsson2011constraint] for syntax, require specialized tools with a learning curve. Their use for a researcher who is not familiar with them can be challenging, and ultimately lead to simply ignoring the existence of the resources.

This paper presents UralicNLP, a Python library, the goal of which is to mask the actual implementation behind a Python interface. This not only lowers the threshold to use the tools provided in the Giellatekno infrastructure but also makes it easier to incorporate them as a part of research code written in Python.

# Functionalities

This section describes the current functionalities of the Python library. At the time of writing, the library focuses on low-level NLP tasks. Additionally, semantic models are provided for a limited number of languages.

## Morphology

The FST models provided in the Giellatekno infrastructure are built on HFST (Helsinki Finite-State Technology) [@linden2013hfst], which is an open-source tool for compiling and running scripts that follow the FST formalism. UralicNLP uses the compiled FST models available through the Online Dictionary of Uralic Languages [@euraleksi].

The library provides morphological analysis on a word level for all supported languages. This means that it will output all the possible morphological readings for an input word form. The morphological analyzers provide typically a lemma, part-of-speech tag and a list morphological tags such as the number and case of the word from. The list of possible readings may include weights indicating the probability of the analysis. However, these are not currently implemented in any of the FST models. For example, for the Finnish word *voit*, the analyzer gives readings *voi* (butter) as a noun in the plural of nominative and *voida* (can) as a verb in the second person of singular.

Given a lemma, part-of-speech tag and morphological tags separated by a plus sign, it is possible to use UralicNLP to generate word forms. This inflection mechanism can be useful in various natural language generation tasks. For instance, giving the Finnish word *kissa*, and the morphological tags *plural* and *genitive*, the library inflects the word as *kissojen*.

## Disambiguation

Whereas the morphological functionality does the analysis only on the word level, the disambiguator applies CG rules to rule out the morphological readings that are not suitable in the context by using the VISL CG-3 tool [@Didriksen]. These CG rules originate from the Giellatekno repository, but they are downloaded through the Online Dictionary of Uralic Languages.

Depending on the language, the disambiguator can often output multiple readings because the rules are not sufficient to fully disambiguate the sentence. It is important to take this into account when using the functionality.


## Lexical Lookup

The API of the Online Dictionary of Uralic Languages provides essentially the same data as in the Giellatekno multilingual XML dictionaries in a JSON format. The actual contents of the data depend on the language, but information such as semantic tags, URLs to audio files, example sentences and translations in multiple languages is oftentimes provided.

In order to use the lexical lookup, the ISO code of the minority language needs to be specified. This will limit the query into the dictionary of that language. Queries can be done either with a lemma or with an inflectional form. It is also possible to query in one of the languages the minority language words are translated to.

## Semantics

UralicNLP provides an easy to use programmatic interface to SemFi and SemUr databases [@yokohama]. These databases contain semantic information of words given their syntactic relations. For example, the database can be used to list out all the verbs that can have *koira* (dog) as a subject together with the frequency of the co-occurrence of the verbs and the noun *koira* in a corpus. SemFi has previously been used in the computationally creative task of poem generation [@poem_gen].

SemUr consists of databases for endangered Uralic languages that have been translated automatically from SemFi. Both of SemFi and SemUr are structurally identical SQLite databases which makes it possible to query them with the same methods provided by UralicNLP.

## Universal Dependency Parser

UralicNLP comes with functionality to parse Treebanks. The parsed Treebanks can be queried effectively with the different universal dependency annotations such as part-of-speech, dependency relation and lemma. The queries support regular expressions. This functionality is useful with the growing number of UD Treebanks available for Uralic languages.


# Distribution

UralicNLP is distributed as an installable package through PyPi with the name uralicNLP[^1]. The source code is released under the Apache open source license on GitHub.

# References

[^1]: pip install uralicNLP

