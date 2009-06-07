from interfaces import ICallsHelper
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.Five import BrowserView
from types import ListType, TupleType
from Acquisition import aq_parent
from Products.CallForContractors.utils import _guessLanguage
from Products.CallForContractors.utils import _doRenamingOfFiles
from Products.CallForContractors.CallForContractors import NEWLY_UPLOADED_MARKER


class CallsHelper(BrowserView):
    implements(ICallsHelper)

    def getRefAndLang(self, context, fieldname=''):
        """ get the reference objects for the given field name and determine their parents' language """
        refs = list()
        if not fieldname:
            return refs
        field = context.getField(fieldname)
        if not field:
            return refs
        references = field.getAccessor(context)()
        if not isinstance(references, (ListType, TupleType)):
            references = [references]
        for ref in references:
            refs.append((ref, aq_parent(ref).Language()))
        return refs

    def checkForNewUploads(self):
        """ check if new files were uploaded, and setLanguage if necessary """
        obj = self.context
        _doRenamingOfFiles(obj)
