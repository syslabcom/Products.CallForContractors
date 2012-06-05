from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class DummySession(dict):
    def set(self, key, value):
        self[key] = value


class CallForContractors(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.CallForContractors')

        import Products.CallForContractors
        self.loadZCML('configure.zcml', package=Products.CallForContractors)

    def setUpPloneSite(self, portal):
        # Needed to make skins work
        applyProfile(portal, 'Products.CMFPlone:plone')

        applyProfile(portal, 'Products.CallForContractors:default')

        # Add a contributor
        roles = ('Member', 'Contributor')
        portal.portal_membership.addMember(
            'contributor', 'secret', roles, [])

        # Use a dummy session
        # portal.REQUEST['SESSION'] = DummySession()

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.CallForContractors')


CALLFORCONTRACTORS_FIXTURE = CallForContractors()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(CALLFORCONTRACTORS_FIXTURE,),
    name="CallForContractors:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CALLFORCONTRACTORS_FIXTURE,),
    name="CallForContractors:Functional")
