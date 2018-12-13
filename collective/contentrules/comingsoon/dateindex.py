# -*- coding: utf-8 -*-
from collective.contentrules.comingsoon import ComingSoonMessageFactory as _
from collective.contentrules.comingsoon.interfaces import IComingSoonSettings
from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from z3c.form import form
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


try:
    from Products.ATContentTypes.interfaces import IFileContent
except ImportError:
    IFileContent = None


class IDateIndexCondition(Interface):
    """Interface for the configurable aspects of a portal type condition.

    This is also used to create add and edit forms, below.
    """

    date_index = schema.Choice(
        title=_(u'Date index'),
        description=_(u'The date index to check for'),
        required=True,
        default='start',
        vocabulary=u'collective.contentrules.comingsoon.alldateindex',
    )


@implementer(IDateIndexCondition, IRuleElementData)
class DateIndexCondition(SimpleItem):
    """The actual persistent implementation of the date index condition.

    Note that we must mix in Explicit to keep Zope 2 security happy.
    """

    date_index = u''
    element = 'comingsoon.condition.DateIndex'

    @property
    def summary(self):
        return _(
            u'Date index is ${idx}',
            mapping=dict(idx=self.date_index)
        )


@implementer(IExecutable)
@adapter(Interface, IDateIndexCondition, Interface)
class DateIndexConditionExecutor(object):
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        index = self.element.date_index
        date = getattr(obj, index, None)
        if not date:
            return False
        if callable(date):
            date = date()
        default_delay = api.portal.get_registry_record(
            interface=IComingSoonSettings, name='delay')
        deadline = DateTime(DateTime().Date()) + default_delay
        return deadline <= date <= deadline + 1


class DateIndexAddForm(AddForm):
    """An add form for date index rule conditions.
    """
    schema = IDateIndexCondition
    label = _(u'Add Date Index Condition')
    description = _(
        u'A date index condition can restrict a rule from '
        u'executing unless the selected date respects deadline delay.'
    )
    form_name = _(u'Configure element')

    def create(self, data):
        c = DateIndexCondition()
        form.applyChanges(self, c, data)
        return c


class DateIndexEditForm(EditForm):
    """An edit form for portal type conditions

    z3c.form does all the magic here.
    """
    schema = IDateIndexCondition
    label = _(u'Edit Date Index Condition')
    description = _(
        u'A date index condition can restrict a rule from '
        u'executing unless the selected date respects deadline delay.'
    )
    form_name = _(u'Configure element')
