from .controlpanel import IConsentControlPanel
from ..tool import Tools
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from plone import api
from ..content.survey import PType as pt
from ..content.question import Activity as act
import time
from email.Utils import formatdate

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
        # GET INFORMATION FROM COOKIE
        r_userId = self.request.cookies.get("_user", "")
        r_sessionId = self.request.cookies.get("_session", "")
        r_questionId = int(self.request.cookies.get("_q_id", -1))
        r_answer = self.request.cookies.get("_q_answer", "")
        r_nav = self.request.cookies.get("_nav", "")
        r_time = self.request.cookies.get("_time", "")
        r_loginStatus = True if len(self.request.cookies.get("__ac", ""))>0 else False
        r_page = self.request.cookies.get("_page", "")
        r_activity = int(self.request.cookies.get("_activity", -1))
        r_query = self.request.cookies.get("_query", "")
        
        #SAVING FEEDBACK
        self.survey = Tools.initSurvey()
        if r_userId is 'undefined':
            r_userId = session
        if r_userId != -1:
            if r_questionId >= 0 and len(r_answer) > 0:
                self.survey.addAnswer(r_userId, r_sessionId, r_questionId, r_answer, r_nav, r_time, self.context, r_loginStatus, r_page, r_query)
        
        # INITIALISING VIEWLET
        if api.user.is_anonymous():
            if r_userId is 'undefined':
                user = self.getSessionId()
            else:
                user = r_userId
        else:
            user = str(api.user.get_current())
        self.question = self.survey.getQuestion(self.context, self.view, self.request["ACTUAL_URL"], user, self.getSessionId(), r_activity)
        self.settings = getUtility(IRegistry).forInterface(IConsentControlPanel)
        
        
        # COOKIE SETTING AND RESETTING, STORED AT CLIENT
        # expiration time: 91` days from now or 3 months
        expiration_seconds = time.time() + (91*24*60*60) 
        expires = formatdate(expiration_seconds, usegmt=True)
        
        # set user activity, browsing or searching
        pageType = self.survey.getPageType(self.context, self.view, self.request["ACTUAL_URL"]) 
        if pageType is pt.search:
            self.request.response.setCookie("_activity", act.search, expires=expires, path='/') 
        elif pageType is pt.browse:
            self.request.response.setCookie("_activity", act.browse, expires=expires, path='/')
        # to track user navigation (back, forward)
        if pageType not in [pt.document,pt.file]:
            self.request.response.setCookie("_nav", "0", expires=expires,  path='/')
        # set question_Id
        if self.question is not None:
            self.request.response.setCookie("_q_id", self.question.getId(), expires=expires, path='/')
        else:
            self.request.response.setCookie("_q_id", "-1", expires=expires, path='/')
        # set answer
        self.request.response.setCookie("_q_answer", "", expires=expires, path='/')
        # set session
        self.request.response.setCookie("_session", self.getSessionId(), expires=expires, path='/')
        # set query
        if pageType not in [pt.document,pt.file]:
            self.request.response.setCookie("_query", self.request["QUERY_STRING"], expires=expires, path='/')
        # set page
        self.request.response.setCookie("_page", self.request["ACTUAL_URL"], expires=expires, path='/')
        
    """
    DATA OUT FOR CLIENT
    """
    def enabled(self):
        """Check whether the consent should be shown or not."""
        return str(self.settings.enabled).lower()
    
    def isAgree(self):
        if self.request.cookies.get("_user", "") == "":
            return "false"
        return "true"
    
    def prevUser(self):
        return self.request.cookies.get("_user", "")
    
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
    
    def isQstAvailable(self):
        if self.question is not None:
            return 'true'
        else:
            return 'false'
    
    
    #END OF DATA OUT FOR CLIENT#
    
    #creating session, in case user do not login
    def setSession(self):
        sdm = self.context.session_data_manager
        if sdm.hasSessionData():
            return
        session = sdm.getSessionData(create=True)
    
    def getContext(self):
        return self.context
    
    def getView(self):
        return self.view
    
    def getManager(self):
        return self.manager
    
    def getPortal(self):
        return api.portal.get()
    
    def getParent(self):
        return self.__parent__
    
    def getAbsoluteUrl(self):
        return self.context.absolute_url() + ' ' + self.request["ACTUAL_URL"] + ' ' + self.request["URL"] + ' ' + self.request["QUERY_STRING"]
    
    def getAnswers(self):
        return self.survey.getAnswers(self.request.cookies.get("_user", ""))