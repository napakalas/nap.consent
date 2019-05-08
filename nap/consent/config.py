"""Common configuration constants
"""
from plone import api

PROJECTNAME = 'nap.consent'

# BBB: remove on deprecation of Plone 4.3
IS_BBB = api.env.plone_version().startswith('4.3')

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
}
