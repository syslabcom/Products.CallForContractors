from zope.interface import Interface


class ICallsListing(Interface):

    def results(obj):
        """Returns a dictionary containing 3 lists: current Calls, ongoing
        Calls, past Calls.
        """


class ICallsHelper(Interface):
    """Helper view for displaying CallsForContractors"""

    def getRefAndLang(context, fieldname):
        """Get the reference objects for the given field name and determine
        their parents' language.
        """

    def checkForNewUploads():
        """Check if new files were uploaded, and setLanguage if necessary."""
