Introduction
============

This content type can be used to present various documents associated with a Call for Contractors. It is
language-aware and has a language fallback.

Boilerplate
===========

First, we must perform some setup.

    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> portal = layer['portal']
    >>> portal_url = portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in.

    >>> browser.open(portal_url + '/login_form')

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = 'admin'
    >>> browser.getControl(name='__ac_password').value = 'secret'
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

    >>> browser.open(portal_url)


Adding a CallForContractors
===========================

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink(url='createObject?type_name=CallForContractors').click()
    >>> 'CallForContractors' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'My Call for Contractors'
    >>> #import pdb;pdb.set_trace()
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'CallForContractors' content item to the portal.

Updating an existing CallForContractors content item
------------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Call for Contractors'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Call for Contractors' in browser.contents
    True

Removing a CallForContractors content item
-----------------------------------

If we go to the home page, we can see a tab with the 'New Call for Contractors' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Call for Contractors' in browser.contents
    True

Now we are going to delete the 'New Call for Contractors' object. First we
go to the contents tab and select the 'New Call for Contractors' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Call for Contractors').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Call for Contractors' tab.

    >>> browser.open(portal_url)
    >>> 'New Call for Contractors' in browser.contents
    False
