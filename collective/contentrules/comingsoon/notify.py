import logging

from DateTime import DateTime
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.event import notify
from zope.publisher.publish import mapply

from plone import api
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView

from collective.contentrules.comingsoon.interfaces import IComingSoonSettings
from collective.contentrules.comingsoon.event import ComingSoonEvent


logger = logging.getLogger('comingsoon.notify')


class NotifyComingSoon(BrowserView):
    """View that notifies contents that are coming soon,
    so that launches IComingSoon rules
    """
    def __call__(self):
        return mapply(self.notify, (), self.request)

    def notify(self, index='start'):
        registry = getUtility(IRegistry)
        delays = registry.forInterface(IComingSoonSettings).delays
        delays = {item['portal_type']: item['delay'] for item in delays}
        catalog = api.portal.get_tool(name='portal_catalog')
        error = 0
        for portal_type, delay in delays.iteritems():
            deadline = DateTime(DateTime().Date()) + delay
            params = {'portal_type': portal_type,
                      index: {'query': (deadline, deadline + 1),
                              'range': 'minmax'},
                      }
            brains = catalog.searchResults(**params)
            for brain in brains:
                try:
                    notify(ComingSoonEvent(brain.getObject()))
                except ConflictError:
                    raise
                except Exception as e:
                    error = 1
                    logger.error("Error when notifying coming soon events : %s" % str(e))

        # default (old behavior)
        default_delay = registry.forInterface(IComingSoonSettings).delay
        deadline = DateTime(DateTime().Date()) + default_delay
        params = {index: {'query': (deadline, deadline + 1),
                          'range': 'minmax'},
                  }
        brains = catalog.searchResults(**params)
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
