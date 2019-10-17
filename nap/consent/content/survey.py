from nap.consent import _
from zope.interface import Interface
from time import time
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from .question import Question
import random
from zope.annotation.interfaces import IAnnotations
from plone import api
from .user import User
from BTrees.OOBTree import OOBTree
from .question import Activity as act

class PType:        # page type -> the type page a question will appear
    browse = 0      # page: ['workspacecontainer at', 'exposurecontainer at'] ['calcium_dynamics', 'cardiovascular_circulation', 'cell_cycle', 'cell_migration', 'circadian_rhythms', 'electrophysiology', 'endocrine', 'excitation-contraction_coupling', 'gene_regulation', 'hepatology', 'immunology', 'ion_transport', 'mechanical_constitutive_laws', 'metabolism', 'myofilament_mechanics', 'neurobiology', 'ph_regulation', 'pkpd', 'protein_modules', 'signal_transduction', 'synthetic_biology']
    search = 1      # page: ['search.pt']
    general = 2     # page: other page
    document = 3    # page: ['workspace at', 'exposure at']
    file = 4        # page: ['exposurefile at']
    allpages = 5    # page: all kind of pages including all mentioned

class Appear:                   # the appearance of a question
    oneForAll = 0               # appear one time for each participant
    onePerSession = 1           # appear one time per session
    onePerSessionPage = 2       # appear one time per session per page

class Survey(Implicit, Persistent, RoleManager, Item):
    security = ClassSecurityInfo()
    checkNumAnswer = 10
    checkNumAnswerSes = 5
    KEY = 'nap.consent.feedback'

    def __init__(self):
        self._questions = []
        self._questionPType = {}
        self._questionAppear = {}

    # multi: *args = choices
    # likert_1, likert_2: *args = q_Low, q_High
    def addQuestion(self, q_Type, q_Question, activity, *args):
        q_Id = len(self._questions)
        question = Question(q_Id, q_Type, q_Question, activity, *args);
        self._questions.append(question)

    def setLastQuestionPages(self, appear, *args):
        lastID = self._questions[-1].getId()
        for arg in args:
            if arg in self._questionPType:
                lstPage = self._questionPType[arg]
            else:
                lstPage = []
            lstPage.append(lastID)
            self._questionPType[arg] = lstPage
        if appear in self._questionAppear:
            lstAppear = self._questionAppear[appear]
        else:
            lstAppear = []
        lstAppear.append(lastID)
        self._questionAppear[appear] = lstAppear

    def getLastQuestionId(self):
        return self._questions[-1].getId()

    def getQuestionTot(self):
        return len(self._questions)

    def getQuestion(self, context, view, actUrl, userId, sessionId, activity):
        if not self.getUserRecord(userId).isActivated():
            return None
        pType = self.getPageType(context, view, actUrl)
        available = []
        #check ALLPAGES questions
        #first priority question, presented when match some condition
        if self.getTotFeedback(userId) >= Survey.checkNumAnswer:
            if self.getTotFeedback(userId,sessionId=sessionId) >= Survey.checkNumAnswerSes:
                for questionId in self._questionPType[PType.allpages]:
                    available += [questionId] if not self.isAnswered(questionId, userId) else []
                if len(available) > 0:
                    return self._questions[random.choice(available)]
        #check GENERAL  page questions
        if pType is PType.general:
            for questionId in self._questionPType[pType]:
                available += [questionId] if not self.isAnswered(questionId, userId) else []

        #check BROWSE page questions
        if pType is PType.browse:
            for questionId in self._questionPType[pType]:
                available += [questionId] if not self.isAnswered(questionId, userId, sessionId=sessionId) else []

        #check SEARCH page questions
        if pType is PType.search:
            for questionId in self._questionPType[pType]:
                if questionId in self._questionAppear[Appear.oneForAll]:
                    if not self.isAnswered(questionId, userId):
                        parentId = self._questions[questionId].getParentId()
                        available += [questionId] if parentId is None else [questionId] if self.isAnswered(parentId, userId) else []
                elif questionId in self._questionAppear[Appear.onePerSession]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId):
                        parentId = self._questions[questionId].getParentId()
                        available += [questionId] if parentId is None else [questionId] if self.isAnswered(parentId, userId, sessionId=sessionId) else []

        #check DOCUMENT or FILE page type
        if pType in [PType.document,PType.file]:
            for questionId in self._questionPType[pType]:
                if questionId in self._questionAppear[Appear.onePerSession]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId):
                        if self._questions[questionId].getActivity() == activity or self._questions[questionId].getActivity() == act.neutral:
                            available += [questionId]
                elif questionId in self._questionAppear[Appear.onePerSessionPage]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId, page=actUrl):
                        if self._questions[questionId].getActivity() == activity or self._questions[questionId].getActivity() == act.neutral:
                            available += [questionId]

        if len(available) > 0:
            available = list(set(available))
            return self._questions[random.choice(available)]

        return None

    #get page type, selected question will be based on the type of the page#
    def getPageType(self, context_, view_, actUrl_):
        context = (str(context_)).lower()
        view = (str(view_)).lower()
        actUrl = (str(actUrl_)).lower()
        wordsSearch = ['search.pt']
        wordsFile = ['exposurefile at']
        wordsDocument = ['workspace at', 'exposure at']
        wordsBrowser = ['workspacecontainer at', 'exposurecontainer at']
        wordsBrowserUrl = ['calcium_dynamics', 'cardiovascular_circulation', 'cell_cycle', 'cell_migration', 'circadian_rhythms', 'electrophysiology', 'endocrine', 'excitation-contraction_coupling', 'gene_regulation', 'hepatology', 'immunology', 'ion_transport', 'mechanical_constitutive_laws', 'metabolism', 'myofilament_mechanics', 'neurobiology', 'ph_regulation', 'pkpd', 'protein_modules', 'signal_transduction', 'synthetic_biology']
        wordsBrowserExp = ['.org/e','.org/exposure']
        if any(word in view for word in wordsSearch):
            return PType.search
        elif any(word in context for word in wordsFile):
            return PType.file
        elif any(word in context for word in wordsDocument):
            return PType.document
        elif any(word in context for word in wordsBrowser):
            return PType.browse
        elif any(word in actUrl for word in wordsBrowserUrl):
            return PType.browse
        elif any(actUrl.endswith(word) for word in wordsBrowserExp):
            return PType.browse
        else:
            return PType.general

    def getUserRecord(self, userId):
        annotations = IAnnotations(api.portal.get())
        if Survey.KEY not in annotations:
            annotations[Survey.KEY] = OOBTree()
        if not annotations[Survey.KEY].has_key(userId):
            annotations[Survey.KEY][userId] = User(userId)
        return annotations[Survey.KEY][userId]

    def isUserExist(self, userId):
        portal = api.portal.get()
        annotations = IAnnotations(api.portal.get())
        if Survey.KEY not in annotations:
            annotations[Survey.KEY] = OOBTree()
            return False
        if annotations[Survey.KEY].has_key(userId):
            return True
        return False


    def getTotFeedback(self,userId,**kwargs):
        userRecord = self.getUserRecord(userId)
        return userRecord.getTotFeedback(**kwargs)

    #isAnswered(questionId, userId, sessionId=sessionId, context=context)
    def isAnswered(self, questionId, userId,  **kwargs):
        userRecord = self.getUserRecord(userId)
        return userRecord.isAnswered(questionId, **kwargs)

    def addAnswer(self, userId, sessionId, questionId, answer, nav, time, context, loginStatus, page, query):
        userRecord = self.getUserRecord(userId)
        return userRecord.addAnswer(sessionId, questionId, answer, nav, time, context, loginStatus, page, query)

    def getSummary(self):
        users = IAnnotations(api.portal.get())[Survey.KEY]
        summary = []
        summary.append("# of participants " + str(len(users)))
        totSession = 0
        totFeedBack = 0
        for user in users.values():
            totSession += user.getTotSession()
            totFeedBack += user.getTotFeedback()
        summary.append("# of sessions " + str(totSession))
        summary.append("# of feedback " + str(totFeedBack))
        return summary

    def cleanUp(self):
        numDelete = 0
        users = IAnnotations(api.portal.get())[Survey.KEY]
        for userId in users.keys():
            user = users.pop(userId)
            del user
            numDelete += 1
        return numDelete

    def disActivateUser(self, userId):
        if self.isUserExist(userId):
            IAnnotations(api.portal.get())[Survey.KEY][userId].setDisActivate()

    def activateUser(self, userId):
        if self.isUserExist(userId):
            IAnnotations(api.portal.get())[Survey.KEY][userId].setActivate()

    def isActivated(self, userId):
        if self.isUserExist(userId):
            return IAnnotations(api.portal.get())[Survey.KEY][userId].isActivated()
        return False

    def getAnswerList(self):
        users = IAnnotations(api.portal.get())[Survey.KEY]
        answerList = []
        for user in users.values():
            answers = user.getAnswerList()
            for answer in answers:
                answerList.append(answer)
        return answerList
