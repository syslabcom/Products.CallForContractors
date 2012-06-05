from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CallForContractors.CallForContractors import NEWLY_UPLOADED_MARKER
#import transaction


def _guessLanguage(context, filename):
    """
    try to find a language abbreviation in the string
    acceptable is a two letter language abbreviation at the end of the
    string prefixed by an _ just before the extension
    """
    if callable(filename):
        filename = filename()

    site = getSite()
    portal_languages = getToolByName(site, 'portal_languages')
    langs = portal_languages.getSupportedLanguages()

    if len(filename) > 3 and '.' in filename:
        elems = filename.split('.')
        name = ".".join(elems[:-1])
        if len(name) > 3 and name[-3] in ['_', '-']:
            lang = name[-2:].strip()
            lang = lang.lower()
            if lang in langs:
                namestem = name[:(len(name) - 2)]
                return lang, namestem, elems[-1]

    return '', filename, ''


def _doRenamingOfFiles(obj):
    if getattr(obj, NEWLY_UPLOADED_MARKER, 0):
        can = obj.getCanonical()
        default_lang = can.Language()
        obj_lang = obj.Language()
        filestems = set()
        # if we're dealing with a translated Call, handle if first, then
        # proceed to the canonical
        if can != obj:
            for item in obj.objectItems():
                lang, namestem, suffix = _guessLanguage(item[1], item[0])
                current_file = item[1]
                if current_file.Language() != lang and lang != '':
                    current_file.setLanguage(lang)
                    filestems.add(namestem)
                    ## Not using the following code, we have linguatools
                    # for that!
                    # transaction.commit()
                    # # create a translation reference
                    # # 1) get the canonical version of the uploaded file
                    # can_filename = namestem + default_lang + '.' + suffix
                    # can_file = getattr(can, can_filename, None)
                    # if can_file:
                    # # 2) the file might have been moved to the translated
                    # #    call - look there
                    #     trans_call = can.getTranslation(lang)
                    #     if trans_call:
                    #         current_file = getattr(trans_call, item[0],
                    #                                current_file)
                    #     current_file.addTranslationReference(can_file)
                    # current_file.reindexObject()
            delattr(obj, NEWLY_UPLOADED_MARKER)

        translated_langs = set()
        for item in can.objectItems():
            lang, namestem, suffix = _guessLanguage(item[1], item[0])
            current_file = item[1]
            if current_file.Language() != lang and lang != '':
                current_file.setLanguage(lang)
                filestems.add(namestem)
                # we need to unset the marker on the translated Calls as well,
                # so remeber the language
                if lang not in (default_lang, obj_lang):
                    translated_langs.add(lang)
                ## Not using the following code, we have linguatools for that!
                # # create a translation reference
                # # 1) get the canonical version of the uploaded file
                # can_filename = namestem + default_lang + '.' + suffix
                # can_file = getattr(can, can_filename, None)
                # if can_file:
                # # 2) the file might have been moved to the translated call -
                # #    look there
                #     trans_call = can.getTranslation(lang)
                #     if trans_call:
                #         import pdb; pdb.set_trace()
                #         current_file = getattr(trans_call, item[0],
                #                                current_file)
                #         # current_file = moved_file
                #     current_file.addTranslationReference(can_file)
                # current_file.reindexObject()
        # delete the marker on the Canonical Call
        # make sure it hasn't been deleted already
        if getattr(can, NEWLY_UPLOADED_MARKER, 0):
            delattr(can, NEWLY_UPLOADED_MARKER)
        can.reindexObject()
        for lang in translated_langs:
            trans = can.getTranslation(lang)
            if trans and getattr(trans, NEWLY_UPLOADED_MARKER, 0):
                delattr(trans, NEWLY_UPLOADED_MARKER)

        for filestem in filestems:
            can_filename = filestem + default_lang + '.' + suffix
            can_file = getattr(can, can_filename, None)
            lt = can_file.restrictedTraverse('@@linguatools-old')
            lt.fixTranslationReference()
