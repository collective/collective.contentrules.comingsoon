# -*- coding: utf-8 -*-
from collective.contentrules.comingsoon.dateindex import DateIndexCondition
from collective.contentrules.comingsoon.dateindex import DateIndexEditForm
from collective.contentrules.comingsoon.interfaces import IComingSoon
from collective.contentrules.comingsoon.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleCondition
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

import unittest


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, obj):
        self.object = obj


class TestDateIndexCondition(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def testRegistered(self):
        element = getUtility(IRuleCondition, name='comingsoon.condition.DateIndex')
        self.assertEqual('comingsoon.condition.DateIndex', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual(IComingSoon, element.for_)
        self.assertEqual(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleCondition, name='comingsoon.condition.DateIndex')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)

        addview.createAndAdd(data={'date_index': 'start'})

        e = rule.conditions[0]
        self.assertIsInstance(e, DateIndexCondition)
        self.assertEqual(e.date_index, u'start')

    def testInvokeEditView(self):
        element = getUtility(IRuleCondition, name='comingsoon.condition.DateIndex')
        e = DateIndexCondition()
        editview = getMultiAdapter((e, self.portal.REQUEST), name=element.editview)
        self.assertTrue(isinstance(editview, DateIndexEditForm))

    def testExecute(self):
        e = DateIndexCondition()
        e.date_index = 'expires'

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal)), IExecutable)
        self.assertEqual(False, ex())

        self.portal.setExpirationDate(DateTime() + 1)

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal)), IExecutable)
        self.assertEqual(True, ex())
