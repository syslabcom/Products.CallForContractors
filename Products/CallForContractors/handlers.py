from Products.Archetypes.atapi import ReferenceField
from Products.CallForContractors.utils import _guessLanguage
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent
from Products.CallForContractors.interfaces import ICallForContractors
from Products.ATContentTypes.interface.file import IATFile
from Products.CallForContractors.CallForContractors import \
    NEWLY_UPLOADED_MARKER
from Products.CallForContractors.utils import _doRenamingOfFiles


def handle_object_translation(obj, event):
    """Copy exisitng references to the target. If a referenced object exits in
    the target's language, use it instead of the canonical's reference.
    """
    obj = obj.getCanonical()
    # get all ReferenceFields
    fields = [x for x in obj.Schema().fields()
              if isinstance(x, ReferenceField)]
    # only handle fields which are not language independent - the others are
    # already taken care of by LinguaPlone
    fields = [x for x in fields if not x.languageIndependent]
    for field in fields:
        refobj = field.getAccessor(obj)()
        # if we get a list, it's not one of our 'section' file reference fields
        if refobj is None or type(refobj) == type(list()):
            continue
        refobjtrans = refobj.getTranslation(event.language, refobj)
        uid = refobjtrans.UID()
        event.target.getField(field.getName()).getMutator(event.target)(uid)


def handle_object_uploaded(event):
    """If a file was uploaded, check if it is a translated version of an
    already referenced file on the canonical. In that case, set the correct
    reference on the translated CallForContractors.
    """
    obj = event.object
    parent = aq_parent(obj)
    if ICallForContractors.providedBy(parent) and IATFile.providedBy(obj):
        canparent = parent.getCanonical()
        langtool = getToolByName(obj, 'portal_languages')
        default_lang = langtool.getDefaultLanguage()
        # determine the file's language by parsing its id
        fname = obj.getId()
        lang, namestem, suffix = _guessLanguage(obj, fname)
        if not lang:
            lang = default_lang

        # look for a possible translation of the CallForContractors
        if lang != default_lang:
            transobj = canparent.getTranslation(lang)
            if transobj:
                fields = [x for x in canparent.Schema().fields()
                          if isinstance(x, ReferenceField)]
                fields = [x for x in fields if not x.languageIndependent]
                for field in fields:
                    refobj = field.getAccessor(canparent)()
                    # if we get a list, it's not one of our 'section' file
                    # reference fields
                    if refobj is None or type(refobj) == type(list()):
                        continue
                    fname = refobj.getFilename()
                    langtrans, namestemtrans, suffixtrans = _guessLanguage(
                        refobj, fname)
                    # is the uploaded file a translated version of a already
                    # referenced file?
                    if namestem == namestemtrans:
                        uid = obj.UID()
                        transobj.getField(
                            field.getName()).getMutator(transobj)(uid)
                transobj.reindexObject()
                setattr(transobj, NEWLY_UPLOADED_MARKER, 1)

        setattr(canparent, NEWLY_UPLOADED_MARKER, 1)

        # Check if the language of the uploaded file is the same as the current
        # object's. If not, then a file with a 'wrong' language was uploaded
        # into the translated CallForContractors
        # Can't do much about it but set the newly-created marker
        if parent != canparent and lang != parent.Language():
            setattr(parent, NEWLY_UPLOADED_MARKER, 1)

        # Tried to setLanguage at this point, but I get an error in
        # manage_cutObjects (_p_jar seems to be None at this point)
        # therefore, setting language is done im handle_edit_begun and in
        # CallsHelper::checkForNewUploads


def handle_edit_begun(obj, event):
    """ Look for the newly-uploaded marker and setLanguages where needed """
    _doRenamingOfFiles(obj)


def handle_object_edited(obj, event):
    """If the canonical object was edited, check if we need to update
    references in the translations.
    """
    if obj.isCanonical():
        fields = [x for x in obj.Schema().fields()
                  if isinstance(x, ReferenceField)]
        # only handle fields which are not language independent - the others
        # are already taken care of by LinguaPlone
        fields = [x for x in fields if not x.languageIndependent]
        translations = obj.getTranslations()
        for field in fields:
            refobj = field.getAccessor(obj)()
            # if we get a list, it's not one of our 'section' file reference
            # fields
            if refobj is None or type(refobj) == type(list()):
                continue
            for tlang in translations.keys():
                tfield = translations[tlang][0].getField(field.getName())
                refobjtrans = refobj.getTranslation(tlang, refobj)
                uid = refobjtrans.UID()
                tfield.getMutator(translations[tlang][0])(uid)


def print_events(event):
    print "print_events:", event


def handle_object_wf_modified(obj, event):
    """If a Call's workflow state is modified, also modify all objects within
    it accordingly.
    """
    pwt = getToolByName(obj, 'portal_workflow')
    for subobj in obj.objectValues():
        actions = [x['id'] for x in pwt.getTransitionsFor(subobj)]
        if event.action in actions:
            pwt.doActionFor(subobj, event.action)
