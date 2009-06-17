from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.Five import fiveconfigure, zcml
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class CallForContractorsLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        ztc.installProduct('CallForContractors')

        ptc.setupPloneSite(products=['CallForContractors'])
        SiteLayer.setUp()


class CallForContractorsTestCase(ptc.PloneTestCase):
    layer = CallForContractorsLayer

class CallForContractorsFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    layer = CallForContractorsLayer

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        ptc.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
