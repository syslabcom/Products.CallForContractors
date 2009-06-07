# -*- coding: utf-8 -*-
#
# File: CallForContractors.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Wolfgang Thomas <thomas@syslab.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope.interface import implements
from interfaces import ICallForContractors

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CallForContractors.config import *

# additional imports from tagged value 'import'
#from Products.RichDocument.content.richdocument import RichDocument, RichDocumentSchema as BaseSchema
from Products.ATContentTypes.content.document import ATDocument, ATDocumentSchema as BaseSchema
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema
from Acquisition import aq_base, aq_parent, aq_base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

##code-section module-header #fill in your manual code here
from Products.SimpleAttachment.widget import AttachmentsManagerWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.ATContentTypes.configuration import zconf
from Products.CallForContractors import CallMessageFactory as _
##/code-section module-header

NEWLY_UPLOADED_MARKER = '_newly_uploaded'
DEFAULT_LANGUAGE = 'en'

schema = Schema((
    DateTimeField(
        name='deadline',
        widget=CalendarWidget(
            size="CalendarWidget",
            label=_(u'call_deadline_label', default=u"Deadline"),
            description=_(u'call_deadline_description', default=u"The deadline for this call"),
        ),
        languageIndependent=True
    ),

    StringField(
        name='author',
        widget=StringWidget(
            size=80,
            label=_(u'call_author_label', default=u"Author"),
            description=_(u'call_author_description', default=u"The author issuing the call"),
        )
    ),

    TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        description = _(u'call_text_description', default=u'Enter the details'),
                        label = _(u'call_text_label', default=u'Details'),
                        rows = 15,
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),

    TextField('info',
              required=False,
              searchable=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        description = _(u'call_info_description', default=u'Enter further information'),
                        label = _(u'call_info_label', default=u'Information'),
                        rows = 15,
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),

    ReferenceField(
        name='contract_notice',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_contract_notice_label', default=u'Contract notice'),
            description=_(u'call_contract_notice_description', default=u'Select the file with the contract notice'),
            allow_search=1,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            base_query=dict(Language=DEFAULT_LANGUAGE),
            ),
        relationship='contract_notice_attachment',
        ),

    ReferenceField(
        name='contract_notice_corrigendum',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_contract_notice_corrigendum_label', default=u'Contract notice corrigendum'),
            description=_(u'call_contract_notice_corrigendum_description', default=u'Select the file with the contract notice corrigendum'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='contract_notice_corrigendum_attachment',
        ),

    ReferenceField(
        name='technical_specifications',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_technical_specifications_label', default=u'Technical specifications'),
            description=_(u'call_technical_specifications_description', default=u'Select the file with the technical specifications'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='technical_specifications_attachment',
        ),

    ReferenceField(
        name='amendments',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_amendments_label', default=u'Amendments'),
            description=_(u'call_amendments_description', default=u'Select the file with the amendments'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='amendments_attachment',
        ),

#    ReferenceField(
#        name='invitation_letter',
#        languageIndependent=0,
#        multiValued=False,
#        widget=ReferenceBrowserWidget(
#            label=_(u'Invitation letter'),
#            description=_(u'Select the file with the invitation letter'),
#            allow_search=0,
#            restrict_browsing_to_startup_directory=1,
#            force_close_on_insert=1,
#            ),
#        relationship='invitation_letter_attachment',
#        ),

    ReferenceField(
        name='agency_responses',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_agency_responses_lable', default=u'Agency responses to requests for clarification'),
            description=_(u'call_agency_responses_description', default=u'Select the file with the agency responses'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='agency_responses_attachment',
        ),

    ReferenceField(
        name='award_notice',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_award_notice_label', default=u'Award notice'),
            description=_(u'call_award_notice_description', default=u'Select the file with the award notice'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='award_notice_attachment',
        ),

    ReferenceField(
        name='award_notice_corrigendum',
        languageIndependent=0,
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label=_(u'call_award_notice_corrigendum_label', default=u'Award notice corrigendum'),
            description=_(u'call_award_notice_corrigendum_description', default=u'Select the file with the award notice corrigendum'),
            allow_search=0,
            restrict_browsing_to_startup_directory=1,
            force_close_on_insert=1,
            ),
        relationship='award_notice_corrigendum_attachment',
        ),
),
)


CallForContractors_schema = BaseSchema.copy() + \
    schema.copy() +\
    ConstrainTypesMixinSchema.copy() +\
    NextPreviousAwareSchema.copy ()

finalizeATCTSchema(CallForContractors_schema)

unwantedFields = ('rights', 'contributors', 'allowDiscussion', 'location',
    'creators', 'creation_date', 'modification_date', 'nextPreviousEnabled',
    'excludeFromNav', 'tableContents', 'presentation', 'language')

for name in unwantedFields:
    CallForContractors_schema[name].widget.visible['edit'] = 'invisible'
    CallForContractors_schema[name].widget.visible['view'] = 'invisible'
    CallForContractors_schema.changeSchemataForField(name, 'default')

class CallForContractors(ATFolder, ATDocument):
    """
    """
    security = ClassSecurityInfo()
    implements(ICallForContractors)
    
    meta_type = 'CallForContractors'
    
    _at_rename_after_creation = True

    schema = CallForContractors_schema
    
    # enable FTP/WebDAV and friends
    PUT = ATDocument.PUT


registerType(CallForContractors, PROJECTNAME)



