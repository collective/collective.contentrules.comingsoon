from zope.interface import Interface
from zope import schema

from collective.contentrules.comingsoon import ComingSoonMessageFactory as _
from zope.component.interfaces import IObjectEvent

class IComingSoon(IObjectEvent):
    """Zope Event to be notified when a plone content
       refers to a date that is coming soon.
    """

class IComingSoonSettings(Interface):

    delay = schema.Int(title=_('label_comingsoon_delay',
                               default=u"Rule handle delay"),
                       description=_("help_comingsoon_delay",
                                     default=u"Type here delay (in days) the coming soon "
                                          "rule will be handled "
                                          "before which an event will start. "
                                          "For example, a delay of 1 significates "
                                          "the event will be handled the day before "
                                          "the event content start date"))