# How to contribute to UralicNLP

## Reporting a bug

Before you report a bug, make sure you are using the latest version of
- UralicNLP *pip install -U uralicNLP*
- [VISL CG](https://mikalikes.men/using-hfst-on-python/)
- Language models *uralicApi.download(language)*

Open up an issue on GitHub

## Fixing a bug

If you have found a bug, feel free to fix it and make a pull request. Give detailed information on what was fixed and how.

## New features

For requesting new features, open up an issue on GitHub. If you want to help in adding a new feature, you can also contact me directly mika.hamalainen📧helsinki.fi

## Adding new languages

If you have your FSTs and CGs distributed through Apertium repository, I can add them easily and they will be updated automatically. Just send me the ISO code by email mika.hamalainen📧helsinki.fi

If your files are not distributed through Apertium, compile them and name them accordingly to Giellatekno naming conventions.

- generator-gt-norm.hfstol
- generator-gt-desc.hfstol
- generator-dict-gt-norm.hfstol (required)
- analyser-gt-norm.hfstol
- analyser-gt-desc.hfstol (required)
- disambiguator.cg3
- metadata.json (required)

Send the files to me by email.

## Making model information more accurate

Every language distributed through akusanat.com has *metadata.json* file. This file contains information about the authors of the FSTs and CGs. However, as most of the tools are from Giellatekno and the AUTHORS and LICENSE contain more often than not \_\_FIXME\_\_ placeholder, this information is mostly missing. If you would like to help in making this information more accurate, feel free to send me a more complete metadata.json by mika.hamalainen📧helsinki.fi

An example of metadata.json

	{
		"license": "CC BY",
		"authors": ["Mr Author"],
		"cite": "Mr Author (2019). A great publication. In a great venue. pages 2-345",
		"website": "https://victorio.uit.no/langtech/trunk/langs/xyz/",
		"acknowledgements": ""
	}

NB. metadata.json can include other keys and subdictionaries as well. The sturcture is used mainly for printing out the information in a human readable format.


