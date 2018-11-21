# -*- coding:utf-8 -*-
from collective.contentrules.comingsoon.testing import INTEGRATION_TESTING
from collective.contentrules.comingsoon.testing import IS_PLONE_5
from collective.contentrules.comingsoon.testing import PLONE_VERSION
from DateTime import DateTime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

import unittest


class ComingSoonRule(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        portal = self.portal

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        mails = self.portal.MailHost = MockMailHost('MailHost')
        mails.smtp_host = 'localhost'
        mails.smtp_port = '25'
        if IS_PLONE_5:
            api.portal.set_registry_record(
                'plone.email_from_name', u'Portal Owner')
            api.portal.set_registry_record(
                'plone.email_from_address', 'portal@test.com')
        else:
            portal.email_from_name = 'Portal Owner'
            portal.email_from_address = 'portal@test.com'
        sm = portal.getSiteManager()
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(component=mails, provided=IMailHost)
        self.mailhost = api.portal.get_tool('MailHost')

        startparam = 'startDate'
        endparam = 'endDate'
        expireparam = 'expirationDate'
        if PLONE_VERSION >= '5':
            startparam = 'start'
            endparam = 'end'
            expireparam = 'expires'

        events = {'eventtoday': {startparam: DateTime(),
                                endparam: DateTime()},
                  'eventtomorrow': {startparam: DateTime() + 1,
                                   endparam: DateTime() + 1},
                  'eventthedayafter': {startparam: DateTime() + 2,
                                       endparam: DateTime() + 2},
                  'eventexpirestoday': {startparam: DateTime() - 5,
                                        endparam: DateTime() - 5,
                                        expireparam: DateTime() + 1}}

        for (event, params) in events.iteritems():
            portal.invokeFactory('Event', event, **params)

        portal.portal_setup.runAllImportStepsFromProfile(
            'profile-collective.contentrules.comingsoon:tests', purge_old=False)

        portal.acl_users.userFolderAddUser(
                'reviewer', 'secret', ['Member', 'Reviewer'], [])
        portal.portal_membership.getMemberById('reviewer').setMemberProperties(
                                                {'email': 'reviewer@null.com'})

    def test_notify(self):
        portal = self.portal
        self.mailhost.reset()
        notify_returns = portal.restrictedTraverse('@@comingsoon-notify')()
        self.assertEqual(notify_returns, 'ok')
        self.assertEqual(len(self.mailhost.messages), 1)
        message = self.mailhost.messages[0]
        self.assertTrue('reviewer@null.com' in message)
        self.assertFalse(portal.eventtoday.absolute_url() in message)
        self.assertTrue(portal.eventtomorrow.absolute_url() in message)
        self.assertFalse(portal.eventthedayafter.absolute_url() in message)
        self.assertFalse(portal.eventexpirestoday.absolute_url() in message)
        
    def test_notify_custom_index(self):
        portal = self.portal
        portal.REQUEST.form['index'] = 'expires'
        self.mailhost.reset()
        notify_returns = portal.restrictedTraverse('@@comingsoon-notify')()
        self.assertEqual(notify_returns, 'ok')
        self.assertEqual(len(self.mailhost.messages), 1)
        message = self.mailhost.messages[0]
        self.assertTrue('reviewer@null.com' in message)
        self.assertFalse(portal.eventtoday.absolute_url() in message)
        self.assertFalse(portal.eventtomorrow.absolute_url() in message)
        self.assertFalse(portal.eventthedayafter.absolute_url() in message)
        self.assertTrue(portal.eventexpirestoday.absolute_url() in message)
