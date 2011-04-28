
def upgrade_1000_to_1100(context):
    """We have added plone.app.registry as dependency
    """
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-plone.app.registry:default')
    setup.runImportStepFromProfile('profile-collective.contentrules.comingsoon:default',
                                   'registry', run_dependencies=False, purge_old=False)
