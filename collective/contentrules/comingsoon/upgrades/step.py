from plone import api


def upgrade_1000_to_1100(context):
    """We have added plone.app.registry as dependency
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runAllImportStepsFromProfile('profile-plone.app.registry:default')
    setup.runImportStepFromProfile('profile-collective.contentrules.comingsoon:default',
                                   'registry', run_dependencies=False, purge_old=False)


def v1101(context):
    """Upgrade to 1101"""
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile('profile-collective.contentrules.comingsoon.upgrades:v1101',
                                   'registry', run_dependencies=False, purge_old=False)
