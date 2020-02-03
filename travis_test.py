#encoding: utf-8
import unittest
from uralicNLP import uralicApi, semfi
from uralicNLP.ud_tools import UD_collection
import codecs

class TestFSTS(unittest.TestCase):

    def setUp(self):
        model_installed = uralicApi.is_language_installed("fin")
        model_installed2 = uralicApi.is_language_installed("swe")
        if not model_installed:
            #download the model, if it is not installed
            uralicApi.download("fin",False)
        if not model_installed2:
            #download the model, if it is not installed
            uralicApi.download("swe",False)

    def test_analysis_unicode(self):
        result = uralicApi.analyze(u"äkkipikainen", "fin",force_local=True)
        self.assertEqual(result[0][0], 'äkkipikainen+A+Sg+Nom')

    def test_analysis(self):
        result = uralicApi.analyze("äkkipikainen", "fin",force_local=True)
        self.assertEqual(result[0][0], 'äkkipikainen+A+Sg+Nom')

    def test_generate_unicode(self):
        result = uralicApi.generate(u"äkkipikainen+A+Sg+Gen", "fin",force_local=True)
        self.assertEqual(result[0][0], 'äkkipikaisen')

    def test_generate(self):
        result = uralicApi.generate("äkkipikainen+A+Sg+Gen", "fin",force_local=True)
        self.assertEqual(result[0][0], 'äkkipikaisen')

    def test_lemmatize_unicode(self):
        result = uralicApi.lemmatize(u"lehmäni", "fin",force_local=True)
        self.assertEqual(result[0], 'lehmä')

    def test_lemmatize(self):
        result = uralicApi.lemmatize("lehmäni", "fin",force_local=True)
        self.assertEqual(result[0], 'lehmä')

    def test_lemmatize_fin(self):
        result = uralicApi.lemmatize("autosaha", "fin",force_local=True)
        self.assertEqual(result[0], 'autosaha')

    def test_lemmatize_fin_bound(self):
        result = uralicApi.lemmatize("autosaha", "fin",force_local=True, word_boundaries=True)
        self.assertEqual(result[0], 'auto|saha')

    def test_lemmatize_swe(self):
        result = uralicApi.lemmatize("livsmedel", "swe",force_local=True)
        self.assertEqual(result[0], 'livsmedel')

    def test_lemmatize_swe_bound(self):
        result = uralicApi.lemmatize("livsmedel", "swe",force_local=True, word_boundaries=True)
        self.assertTrue('livs|medel' in result[0])

class TestUD(unittest.TestCase):
    def setUp(self):
        self.ud = UD_collection(codecs.open("test_data/fi_test.conllu","r",encoding="utf-8"))

    def test_find_sentences(self):
        sentences = self.ud.find_sentences(query={"lemma": u"suuri"})
        self.assertEqual(1, len(sentences))

    def test_find_non_existing_sentences(self):
        sentences = self.ud.find_sentences(query={"lemma": u"tuuri"})
        self.assertEqual(0, len(sentences))

    def test_find_words(self):
        words = self.ud.find_sentences()[0].find(query={"pos": "AUX"})
        self.assertEqual(3, len(words))

    def test_find_word(self):
        words = self.ud.find_sentences()[0].find(query={"form": u"sitä"})
        self.assertEqual("se", words[0].get_attribute("lemma"))

    def test_find_non_existing_word(self):
        words = self.ud.find_sentences()[0].find(query={"form": u"hattua"})
        self.assertEqual(0, len(words))

class TestSemfi(unittest.TestCase):
    def setUp(self):
        model_installed = semfi.is_language_installed("kpv")
        if not model_installed:
            semfi.download("kpv",False)

    def test_model_downloaded(self):
        installed = semfi.is_language_installed("kpv")
        self.assertEqual(installed, True)

    def test_get_word(self):
        w = semfi.get_word("кань", "N", "kpv")
        self.assertIsNotNone(w)

    def tes_non_word(self):
        w = semfi.get_word("kisseli", "N", "kpv")
        self.assertIsNone(w)


if __name__ == '__main__':
    unittest.main()