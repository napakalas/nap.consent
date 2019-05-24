from nap.consent import _
from zope.interface import Interface

from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item


class QType:
    likert_1 = 0
    likert_2 = 1
    multi = 2
    text = 3

class Activity:
    browse = 0
    search = 1
    neutral = 3


class Question(Implicit, Persistent, RoleManager, Item):    
    # multi: *args = choices
    # likert_1, likert_2: *args = q_Low than q_High
    def __init__(self, qId, qType, question, activity, parentId, *args):
        self._id = qId
        self._type = qType
        self._question = question
        self._activity = activity
        self._parentId = parentId
        if qType is QType.likert_1 or qType is QType.likert_2:
            self._low = args[0]
            self._high = args[1]
        else:
            self._low = None
            self._high = None
        if qType is QType.multi:
            self._choices = args
        else:
            self._choices = None
        
    def getId(self):
        return self._id
    
    def getType(self):
        return self._type
    
    def getQuestionText(self):
        return self._question
    
    def getActivity(self):
        return self._activity
    
    def getParentId(self):
        return self._parentId
    
    def getLow(self):
        return self._low
    
    def getHigh(self):
        return self._high
    
    def getChoices(self):
        if self._type is QType.likert_1:
            return ('0','1','2','3','4')
        if self._type is QType.likert_2:
            return ('0','1','2','3','4')
        if self._type is QType.multi:
            return self._choices
        return self._choices
