from Products.CallForContractors.browser.interfaces import ICallsListing
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from Products.Five import BrowserView
from DateTime import DateTime
from DocumentTemplate import sequence


class CallsSortedListing(BrowserView):
    implements(ICallsListing)

    def results(self):
        context = self.context
        portal_catalog = getToolByName(context, 'portal_catalog')
        res = portal_catalog({
            'portal_type': 'CallForContractors',
            'sort_on': 'effective',
            #'Language': 'all',
            'sort_order': 'reverse'})
        effRes = []
        cres = []
        ores = []
        ares = []
        date = DateTime()

        for r in res:
            try:
                o = r.getObject()
            except:
                continue
            pastEffective = (r.effective is None or r.effective == ''
                             or r.effective <= date )
            beforeExpiration = (r.expires is None or r.expires == ''
                                or r.expires >= date )
            if r.effective is None and r.expires is None:
                continue

            if pastEffective:
                if beforeExpiration:
                    effRes.append(r)
                    if o.deadline > date:
                        cres.append(r)
                    else:
                        ores.append(r)
                else:
                    ares.append(r)
        cres = sequence.sort(cres, (('effective', 'cmp', 'desc'),
                                    ('CreationDate', 'cmp', 'desc')))
        ores = sequence.sort(ores, (('effective', 'cmp', 'desc'),
                                    ('CreationDate', 'cmp', 'desc')))
        return dict(current=cres, ongoing=ores, archive=ares)
