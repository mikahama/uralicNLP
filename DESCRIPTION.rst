=====================
Korp API for Python
=====================

This library provides an easy way to query `Korp <https://spraakbanken.gu.se/swe/forskning/infrastruktur/korp/>`_ systems for language corpora. This library is brought to you by `Mika Hämäläinen <https://mikakalevi.com>`_.

*****
Usage
*****
You can initialise Korp with either service_name (`språkbanken <https://spraakbanken.gu.se/korp/#?lang=sv>`_, `kielipankki <https://korp.csc.fi/>`_ or `GT <http://gtweb.uit.no/korp/>`_) or url to your Korp's API interface such as https://korp.csc.fi/cgi-bin/korp.cgi .

An example for getting all concordances for North Sami corpora in Giellatekno Korp for query *[pos="A"] "go" [pos="N"]*.

    ``from korp import Korp``

    ``korppi = Korp(service_name="GT") #uses Giellatekno``

    ``corpora = korppi.list_corpora("SME") #lists corpora returns the ones starting with the North Sami language code``

    ``number_of_results, concordances = korppi.all_concordances('[pos="A"] "go" [pos="N"]', corpora)``

****************
More information
****************

For more information, see `the GitHub page <https://github.com/mikahama/python-korp>`_ and `Wiki for tutorials <https://github.com/mikahama/python-korp/wiki>`_.
