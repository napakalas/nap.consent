from nap.consent import _
from zope.interface import Interface
from zope.interface import implements
from time import time
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from .question import Question
from .question import QType
import random

class ISurvey(Interface):
    """A survey for PMR."""

class Survey(Implicit, Persistent, RoleManager, Item):
    
    implements(ISurvey)
    security = ClassSecurityInfo()
    def __init__(self):
        self._count = 0
        self._prevUser = ''
        self._prevTimestamp = ''
        self.__questions = []
        
    def increment(self, timestamp, userId):
        if self._prevUser != userId or self._prevTimestamp != timestamp:
            self._count = self._count + 1
            self._prevUser = userId
            self._prevTimestamp = timestamp
        
    def getCount(self):
        return self._count
    
    # multi: *args = choices
    # likert_1, likert_2: *args = q_Low, q_High
    def addQuestion(self, q_Type, q_Question, *args):
        q_Id = len(self.__questions)
        question = Question(q_Id, q_Type, q_Question, *args);
        self.__questions.append(question)
        
    def getQuestion(self):
        ran = random.randint(0, 15)
        return self.__questions[ran]
    
    def getQuestionTot(self):
        return len(self.__questions)

