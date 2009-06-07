import unittest
import doctest
import zope.testing
from base import CallForContractorsFunctionalTestCase, CallForContractorsTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class LMSTestCase(CallForContractorsTestCase):

    def test_lmssupport(self):
        from Products.CMFLinkChecker.retrievers import RichTextRetriever
        self.failUnless('CallForContractors' in RichTextRetriever.defaults)
    
    
    
def test_suite():
    return unittest.TestSuite((
            Suite('tests/CallForContractors.txt',
                   optionflags=OPTIONFLAGS,
                   package='Products.CallForContractors',
                   test_class=CallForContractorsFunctionalTestCase) ,



        ))