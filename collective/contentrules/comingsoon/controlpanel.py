# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel

from collective.contentrules.comingsoon.interfaces import IComingSoonSettings
from collective.contentrules.comingsoon import ComingSoonMessageFactory as _


class ComingSoonControlPanelEditForm(controlpanel.RegistryEditForm):

    schema = IComingSoonSettings
    label = _(u"Coming soon content rule settings")
    description = _(u"help_coming_soon_settings_editform",
                    default=u"You can set here some options related to the "
                             "coming soon rule type.")


class ComingSoonControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ComingSoonControlPanelEditForm
