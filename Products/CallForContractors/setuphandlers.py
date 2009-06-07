# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
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

__author__ = """Syslab.com GmbH <info@syslab.com>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('CallForContractors: setuphandlers')
from config import PROJECTNAME
from config import DEPENDENCIES
from Products.CMFCore.utils import getToolByName
from Products.SimpleAttachment.setuphandlers import registerImagesFormControllerActions
from Products.SimpleAttachment.setuphandlers import registerAttachmentsFormControllerActions


def installAttachmentSupport(context):
    """ install attachment handlers """
    pass

