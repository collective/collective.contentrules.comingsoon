from five import grok
from plone import api
from Products.PluginIndexes.interfaces import IDateIndex
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


try:
    from Products.DateRecurringIndex.index import IDateRecurringIndex
except ImportError:
    class IDateRecurringIndex(Interface):
        """Fake interface
        """


class DelayVocabulary(grok.GlobalUtility):
    """Vocabulary for delay - integers between 0 and 31"""
    grok.implements(IVocabularyFactory)
    grok.name("DelayVocabulary")

    def __call__(self, context):
        l = range(0, 32)
        items = zip(l, l)
        return SimpleVocabulary.fromItems(items)


def AllDateIndexVocabulary(context):
    """Vocabulary factory for all date indexes."""
    catalog = api.portal.get_tool('portal_catalog')
    return SimpleVocabulary([
        SimpleTerm(value=index.id)
        for index in catalog.getIndexObjects()
        if IDateIndex.providedBy(index) or
           IDateRecurringIndex.providedBy(index)
    ])


