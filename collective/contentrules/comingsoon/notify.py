# -*- coding: utf-8 -*-
from DateTime import DateTime
from collective.contentrules.comingsoon.event import ComingSoonEvent
from collective.contentrules.comingsoon.interfaces import IComingSoonSettings
from plone import api
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.component import getUtility
from zope.event import notify
from zope.publisher.publish import mapply

import logging


logger = logging.getLogger('comingsoon.notify')


class NotifyComingSoon(BrowserView):
    """View that notifies contents that are coming soon,
    so that launches IComingSoon rules
    """
    def __call__(self):
        self.setup()
        return mapply(self.notify, (), self.request)

    def setup(self):
        self.registry = getUtility(IRegistry)
        self.catalog = api.portal.get_tool(name='portal_catalog')

    def notify(self, index='start'):
        error = 0
        indexes = self.get_dateindexes()
        for index in indexes:
            error += self.notify_delays(index)
            error += self.notify_delay(index)
        if not indexes:
            error += self.notify_delays(index)
            error += self.notify_delay(index)
        if error:
            return 'error'
        return 'ok'

    def get_dateindexes(self):
        indexes = set()
        storage = getUtility(IRuleStorage)
        if storage is None or not storage.active:
            return indexes
        for rule in storage.values():
            for condition in rule.conditions:
                data = IRuleElementData(condition)
                if data.element != 'comingsoon.condition.DateIndex':
                    continue
                indexes.add(data.date_index)
        return indexes

    def notify_delays(self, index):
        error = 0
        delays = self.registry.forInterface(IComingSoonSettings).delays
        if not delays:
            return error
        delays = {item['portal_type']: item['delay'] for item in delays}
        for portal_type, delay in delays.iteritems():
            deadline = DateTime(DateTime().Date()) + delay
            params = {
                'portal_type': portal_type,
                index: {
                    'query': (deadline, deadline + 1),
                    'range': 'minmax',
                },
            }
            brains = self.catalog.searchResults(**params)
            for brain in brains:
                try:
                    notify(ComingSoonEvent(brain.getObject()))
                except ConflictError:
                    raise
                except Exception as e:
                    error = 1
                    logger.error("Error when notifying coming soon events : %s" % str(e))
        return error

    def notify_delay(self, index):
        # default (old behavior)
        error = 0
        default_delay = self.registry.forInterface(IComingSoonSettings).delay
        deadline = DateTime(DateTime().Date()) + default_delay
        params = {
            index: {
                'query': (deadline, deadline + 1),
                'range': 'minmax',
            },
        }
        brains = self.catalog.searchResults(**params)
        for brain in brains:
            try:
                notify(ComingSoonEvent(brain.getObject()))
            except ConflictError:
                raise
            except Exception as e:
                error = 1
                logger.error("Error when notifying coming soon events : %s" % str(e))
        return error
