from five import grok

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class DelayVocabulary(grok.GlobalUtility):
    """Vocabulary for delay - integers between 0 and 31"""
    grok.implements(IVocabularyFactory)
    grok.name("DelayVocabulary")

    def __call__(self, context):
        l = range(0, 32)
        items = zip(l, l)
        return SimpleVocabulary.fromItems(items)
