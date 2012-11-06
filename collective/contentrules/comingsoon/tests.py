import unittest

from DateTime import DateTime

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

import collective.contentrules.comingsoon


ptc.setupPloneSite()

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.contentrules.comingsoon)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


class ComingSoonRule(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        portal = self.portal

        portal.email_from_address = 'portal@test.com'
        mockmailhost = MockMailHost('MailHost')
        portal.MailHost = mockmailhost
        sm = portal.getSiteManager()
        sm.registerUtility(component=mockmailhost, provided=IMailHost)

        portal.invokeFactory('Event', 'eventtoday',
                             startDate=DateTime(),
                             endDate=DateTime())
        portal.invokeFactory('Event', 'eventtomorrow',
                             startDate=DateTime() + 1,
                             endDate=DateTime() + 1)
        portal.invokeFactory('Event', 'eventthedayafter',
                             startDate=DateTime() + 2,
                             endDate=DateTime() + 2)
        portal.invokeFactory('Event', 'eventexpirestoday',
                             startDate=DateTime() - 5,
                             endDate=DateTime() - 5,
                             expirationDate=DateTime()+1,
                             )
        portal.portal_setup.runAllImportStepsFromProfile(
            'profile-collective.contentrules.comingsoon:tests', purge_old=False)

        portal.acl_users.userFolderAddUser(
                'reviewer', 'secret', ['Member', 'Reviewer'], [])
        portal.portal_membership.getMemberById('reviewer').setMemberProperties(
                                                {'email': 'reviewer@null.com'})

    def test_notify(self):
        portal = self.portal
        mailhost = portal.MailHost
        portal.restrictedTraverse('@@comingsoon-notify')()

        self.assertEqual(len(mailhost.messages), 1)
        message = mailhost.messages[0]
        self.assertTrue('reviewer@null.com' in message)
        self.assertFalse(portal.eventtoday.absolute_url() in message)
        self.assertTrue(portal.eventtomorrow.absolute_url() in message)
        self.assertFalse(portal.eventthedayafter.absolute_url() in message)
        self.assertFalse(portal.eventexpirestoday.absolute_url() in message)
        
    def test_notify_custom_index(self):
        portal = self.portal
        mailhost = portal.MailHost
        portal.REQUEST.form['index'] = 'expires'
        portal.restrictedTraverse('@@comingsoon-notify')()
        self.assertEqual(len(mailhost.messages), 1)
        message = mailhost.messages[0]
        self.assertTrue('reviewer@null.com' in message)
        self.assertFalse(portal.eventtoday.absolute_url() in message)
        self.assertFalse(portal.eventtomorrow.absolute_url() in message)
        self.assertFalse(portal.eventthedayafter.absolute_url() in message)
        self.assertTrue(portal.eventexpirestoday.absolute_url() in message)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ComingSoonRule))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
