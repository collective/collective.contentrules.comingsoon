  # -*- extra stuff goes here -*-

from zope.i18nmessageid import MessageFactory


ComingSoonMessageFactory = MessageFactory('collective.contentrules.comingsoon')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
