from .controlpanel import IConsentControlPanel
from ..tool import Tools
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from plone import api

class ConsentViewlet(ViewletBase):
            
    def update(self):
        super(ConsentViewlet, self).update()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IConsentControlPanel)
        
    def enabled(self):
        """Check whether the consent should be shown or not."""
        return str(self.settings.enabled).lower()

    def title(self):
        """Return the title of participation offer."""
        return self.settings.title

    def text(self):
        """Return the purpose of study"""
        return self.settings.text
    
    def user(self):
        if api.user.is_anonymous():
            return ''
        else:
            return str(api.user.get_current())