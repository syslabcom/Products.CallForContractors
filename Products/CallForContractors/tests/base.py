from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('CallForContractors')
ztc.installProduct('CMFLinkChecker')
ztc.installProduct('ZCatalog')

ptc.setupPloneSite(products=['CallForContractors', 'CMFLinkChecker'])

class CallForContractorsTestCase(ptc.PloneTestCase):
    pass
    
class CallForContractorsFunctionalTestCase(ptc.FunctionalTestCase):
    pass