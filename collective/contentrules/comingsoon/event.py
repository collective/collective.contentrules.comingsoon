from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from collective.contentrules.comingsoon.interfaces import IComingSoon


class ComingSoonEvent(ObjectEvent):
    """Zope Event to be notified when a plone content
       refers to a date that is coming soon.
    """

    implements(IComingSoon)
