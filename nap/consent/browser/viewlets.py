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
        r_userId = self.request.cookies.get("_user", -1)
        r_sessionId = self.request.cookies.get("_session", "")
        try:
            r_questionId = int(self.request.cookies.get("_q_id", -1))
        except:
            r_questionId = -1
        r_answer = self.request.cookies.get("_q_answer", "")
        r_nav = self.request.cookies.get("_nav", "")
        r_time = self.request.cookies.get("_time", "")
        r_loginStatus = True if len(
            self.request.cookies.get("__ac", "")) > 0 else False
        r_page = self.request.cookies.get("_page", "")
        try:
            r_activity = int(self.request.cookies.get("_activity", -1))
        except:
            r_activity = -1
        r_query = self.request.cookies.get("_query", "")

        # SAVING FEEDBACK
        survey = Tools.initSurvey()
        if r_userId == 'undefined':
            r_userId = r_sessionId
        if r_userId != -1:
            if r_questionId >= 0 and len(r_answer) > 0:
                survey.addAnswer(r_userId, r_sessionId, r_questionId, r_answer, r_nav, r_time, str(
                    self.context), r_loginStatus, r_page, r_query)

        # WITHDRAW FROM SURVEY
        userId = str(api.user.get_current())
        if r_userId == -1 and not api.user.is_anonymous():
            survey.disActivateUser(str(api.user.get_current()))
        elif r_userId != -1 and not api.user.is_anonymous() and not survey.isActivated(userId):
            survey.activateUser(str(api.user.get_current()))

        # INITIALISING VIEWLET
        if api.user.is_anonymous():
            if r_userId == 'undefined':
                userId = self.getSessionId()
            else:
                userId = r_userId

        # get a new question
        if r_userId != -1:  # is a participant
            page = self.request["ACTUAL_URL"]
            page = page[page.find('pmr') + 4:] if 'pmr' in page else page
            self.question = survey.getQuestion(
                self.context, self.view, page, userId, self.getSessionId(), r_activity)
        else:
            self.question = None
        self.settings = getUtility(
            IRegistry).forInterface(IConsentControlPanel)

        # COOKIE SETTING AND RESETTING, STORED AT CLIENT
        # expiration time: 91` days from now or 3 months
        expiration_seconds = time.time() + (91 * 24 * 60 * 60)
        expires = formatdate(expiration_seconds, usegmt=True)

        # set user activity, browsing or searching
        pageType = survey.getPageType(
            self.context, self.view, self.request["ACTUAL_URL"])
        if pageType is pt.search:
            self.request.response.setCookie(
                "_activity", act.search, expires=expires, path='/')
        elif pageType is pt.browse:
            self.request.response.setCookie(
                "_activity", act.browse, expires=expires, path='/')
        # to track user navigation (back, forward)
        if pageType not in [pt.document, pt.file]:
            self.request.response.setCookie(
                "_nav", "0", expires=expires,  path='/')
        # set question related cookies
        if self.question is not None:
            self.request.response.setCookie(
                "_q_id", self.question.getId(), expires=expires, path='/')
            page = self.request["ACTUAL_URL"]
            page = page[page.find('.org/') + 5:] if '.org/' in page else page[page.find(
                '/pmr/') + 5:] if '/pmr/' in page else page
            self.request.response.setCookie(
                "_page", page, expires=expires, path='/')
            self.request.response.setCookie(
                "_q_type", self.getQuestionType(), expires=expires, path='/')
            self.request.response.setCookie(
                "_q_text", self.getQuestionText(), expires=expires, path='/')
            self.request.response.setCookie(
                "_q_low", self.getLow(), expires=expires, path='/')
            self.request.response.setCookie(
                "_q_high", self.getHigh(), expires=expires, path='/')
            self.request.response.setCookie(
                "_q_choices", self.getChoices(), expires=expires, path='/')
        else:
            self.request.response.setCookie(
                "_q_id", "-1", expires=expires, path='/')
        # set answer
        self.request.response.setCookie(
            "_q_answer", "", expires=expires, path='/')
        # set session
        self.request.response.setCookie(
            "_session", self.getSessionId(), expires=expires, path='/')
        # set query
        if pageType not in [pt.document, pt.file]:
            self.request.response.setCookie(
                "_query", self.request["QUERY_STRING"], expires=expires, path='/')

    """ DATA OUT FOR CLIENT """

    def enabled(self):
        """Check whether the consent should be shown or not."""
        return str(self.settings.enabled).lower()

    def isAgree(self):
        if self.request.cookies.get("_user", "") == "":
            return "false"
        return "true"

    def isQstAvailable(self):
        if self.question is not None:
            return "true"
        else:
            return "false"

    """ FUNCTION FOR SUPPLY COOKIES DATA """

    def getBrowserId(self):
        sdm = self.context.session_data_manager
        browser_id = sdm.getBrowserIdManager().getBrowserId()
        return str(browser_id)

    def getSessionId(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData()
        return str(session.id)

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

    def getGeneralQuestion(self):
        general_question = Tools.survey.getGeneralQuestion()
        return general_question.getId(), general_question.getType(), general_question.getQuestionText()
