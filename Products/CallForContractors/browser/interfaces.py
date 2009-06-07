from zope.interface import Interface, Attribute

class ICallsListing(Interface):

    def results(obj):
        """ returns a dictionary containing 3 lists: current Calls, ongoing Calls, past Calls
        """

class ICallsHelper(Interface):
    """ Helper view for displaying CallsForContractors """

    def getRefAndLang(context, fieldname):
        """ get the reference objects for the given field name and determine their parents' language """

    def checkForNewUploads():
        """ check if new files were uploaded, and setLanguage if necessary """