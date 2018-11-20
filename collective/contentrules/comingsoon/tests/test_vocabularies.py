# -*- coding: utf-8 -*-
from collective.contentrules.comingsoon.testing import INTEGRATION_TESTING
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_alldateindex_vocabulary(self):
        name = 'collective.contentrules.comingsoon.alldateindex'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        indexes = util(self.portal)
        self.assertGreaterEqual(len(indexes), 7)
