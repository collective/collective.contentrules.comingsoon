from zope.component.interfaces import IObjectEvent
from zope.interface import Interface
from zope import schema

from plone.autoform.directives import widget

from collective.contentrules.comingsoon import ComingSoonMessageFactory as _
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


class IComingSoon(IObjectEvent):
    """Zope Event to be notified when a plone content
       refers to a date that is coming soon.
    """


class IDelayTableRowSchema(Interface):
    """Schema for the delays datagridfield"""
    portal_type = schema.Choice(
                title=_(u"Portal type"),
                vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
                required=False,
                )
    delay = schema.Choice(
                title=_(u"Delay"),
                vocabulary="DelayVocabulary",
                required=False,
                )


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

    delays = schema.List(
        title=_("Delays"),
        value_type=DictRow(title=_(u'Per content types delays'),
                           schema=IDelayTableRowSchema),
        description=_("help_comingsoon_delay",
                      default=u"For each content type, type here delay "
                               "(in days) the coming soon "
                               "rule will be handled "
                               "before which an event will start. "
                               "For example, a delay of 1 signify "
                               "the event will be handled the day before "
                               "the event content start date")
        )
    widget(delays=DataGridFieldFactory)
