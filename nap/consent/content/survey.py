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

class PType:
    browse = 0
    search = 1
    general = 2
    document = 3
    file = 4
    allpages = 5

class Appear:
    oneForAll = 0
    onePerSession = 1
    onePerSessionPage = 2

class Survey(Implicit, Persistent, RoleManager, Item):
    
    security = ClassSecurityInfo()
    checkNumAnswer = 5
    checkNumAnswerSes = 2
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
        lastID = len(self._questions)-1
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
            
    def getQuestionTot(self):
        return len(self._questions)
        
    def getQuestion(self, context, view, actUrl, userId, sessionId, activity):
        if not self.getUserRecord(userId).isActivated():
            return None
        
        pType = self.getPageType(context, view, actUrl)
        #check ALLPAGES questions
        if self.getTotFeedback(userId) >= Survey.checkNumAnswer:
            if self.getTotFeedback(userId,sessionId=sessionId) >= Survey.checkNumAnswerSes:
                for questionId in self._questionPType[PType.allpages]:
                    if not self.isAnswered(questionId, userId):
                        return self._questions[questionId]
        #check GENERAL page questions
        if pType is PType.general:
            #return self._questions[random.choice(self._questionPType[PType.general])]
            for questionId in self._questionPType[PType.general]:
                if self.isAnswered(questionId, userId) is False:
                    return self._questions[questionId]
        #check BROWSE page questions
        if pType is PType.browse:
            for questionId in self._questionPType[PType.browse]:
                if not self.isAnswered(questionId, userId, sessionId=sessionId):
                    return self._questions[questionId]
        #check SEARCH page questions
        if pType is PType.search:
            available = []
            for questionId in self._questionPType[PType.search]:
                if questionId in self._questionAppear[Appear.oneForAll]:
                    if not self.isAnswered(questionId, userId):
                        parentId = self._questions[questionId].getParentId()
                        if parentId is None:
                            available.append(questionId)
                        elif self.isAnswered(parentId, userId):
                            available.append(questionId)
                elif questionId in self._questionAppear[Appear.onePerSession]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId):
                        parentId = self._questions[questionId].getParentId()
                        if parentId is None:
                            available.append(questionId)
                        elif self.isAnswered(parentId, userId, sessionId=sessionId):
                            available.append(questionId)
                        
            if len(available) > 0:
                return self._questions[random.choice(available)]
        #check DOCUMENT or FILE page type
        if pType in [PType.document,PType.file]:
            available = []
            for questionId in self._questionPType[pType]:
                if questionId in self._questionAppear[Appear.onePerSession]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId):
                        if self._questions[questionId].getActivity() == activity:
                            available.append(questionId)
                elif questionId in self._questionAppear[Appear.onePerSessionPage]:
                    if not self.isAnswered(questionId, userId, sessionId=sessionId, context=context):
                        if self._questions[questionId].getActivity() == activity:
                            available.append(questionId)
            if len(available) > 0:
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
    
    def getAnswers(self, userId):
        return self.getUserRecord(userId).getAnswers()
        
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
        condition = 'False'
        users = IAnnotations(api.portal.get())[Survey.KEY]
        for userId in users.keys():
            try:
                user = users.pop(userId)
                del user
                condition = "True"
            except:
                condition = "True"
        return condition
        
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