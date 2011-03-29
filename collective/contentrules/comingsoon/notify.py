import logging

from DateTime import DateTime
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.event import notify

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from collective.contentrules.comingsoon.interfaces import IComingSoonSettings
from collective.contentrules.comingsoon.event import ComingSoonEvent


logger = logging.getLogger('comingsoon.notify')

class NotifyComingSoon(BrowserView):
    """View that notifies contents that are coming soon,
    so that launches IComingSoon rules
    """

    def notify(self):

        registry = getUtility(IRegistry)
        delay = registry.forInterface(IComingSoonSettings).delay

        catalog = getToolByName(self.context, 'portal_catalog')

        deadline = DateTime(DateTime().Date()) + delay
        brains = catalog.searchResults(start={'query': (deadline, deadline + 1),
                                              'range': 'minmax'})
        error = 0
        for brain in brains:
            try:
                notify(ComingSoonEvent(brain.getObject()))
            except ConflictError:
                raise
            except Exception as e:
                error = 1
                logger.error("Error when notifying coming soon events : %s" % str(e))

        if error:
            return 'error'
        else:
            return 'ok'