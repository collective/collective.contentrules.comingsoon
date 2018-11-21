# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


IS_PLONE_5 = api.env.plone_version().startswith('5')
PLONE_VERSION = api.env.plone_version()

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if IS_PLONE_5:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
        # Load ZCML
        import collective.contentrules.comingsoon
        self.loadZCML(package=collective.contentrules.comingsoon)

    def setUpPloneSite(self, portal):
        if IS_PLONE_5:
            self.applyProfile(portal, 'plone.app.contenttypes:default')
        self.applyProfile(portal, 'collective.contentrules.comingsoon:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.contentrules.comingsoon:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.contentrules.comingsoon:Functional',
)
