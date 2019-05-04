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
        
class SurveyViewlet(ViewletBase):
    def __init__(self, context, request, view, manager):
        super(SurveyViewlet, self).__init__(context, request, view, manager)
    
    def update(self):
        super(SurveyViewlet, self).update()
        # cookie setting to indicate browser forward or backward navidation
        self.request.response.setCookie("_nav", '0',  path='/')
        #self.setSession()
        self.survey = Tools.initSurvey()
        self.question = self.survey.getQuestion()
        self.settings = getUtility(IRegistry).forInterface(IConsentControlPanel)
        # get information from cookies
        self.collectCookies()
        
    #DATA OUT FOR CLIENT#
    def enabled(self):
        """Check whether the consent should be shown or not."""
        return str(self.settings.enabled).lower()
    
    def isAgree(self):
        if self.request.cookies.get("_user", "") == "":
            return "false"
        return "true"
    
    def prevUser(self):
        return self.request.cookies.get("_user", "")
    
    def isLogin(self):
        if self.request.cookies.get("__ac", "") == "":
            return "false"
        return "true"
    
    def getBrowserId(self):
        sdm = self.context.session_data_manager
        browser_id = sdm.getBrowserIdManager().getBrowserId()
        return str(browser_id)
    
    def getSession(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData()
        return str(session)
    
    def getSessionId(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData()
        return str(session.id)
    
    def getCookieId(self):
        return self.request.cookies.get("__ac", "")
    
    def getQuestionType(self):
        return self.question.getType()
    
    def getQuestionText(self):
        return self.question.getQuestionText()
    
    def getLow(self):
        return self.question.getLow()
    
    def getHigh(self):
        return self.question.getHigh()
    
    def getChoices(self):
        return self.question.getChoices()
    
    
    #END OF DATA OUT FOR CLIENT#
    
    #creating session, in case user do not login
    def setSession(self):
        sdm = self.context.session_data_manager
        if sdm.hasSessionData():
            return
        session = sdm.getSessionData(create=True)
        
    #DATA IN TO SAVE#
    #collecting information from cookie
    def collectCookies(self):
        timestamp = self.request.cookies.get("_time", "")
        userId = self.request.cookies.get("_user", "")
        #self.survey.increment(timestamp, userId)
    #END OF DATA IN TO SAVE#
    
    def getCount(self):
        #return self.survey.getCount();
        return 10
    
    def getContext(self):
        return self.context
    
    def getView(self):
        return self.view
    
    def getManager(self):
        return self.manager