from nap.consent import _
from time import time
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from BTrees.OOBTree import OOBTree
from BTrees.OOBTree import OOTreeSet

class Session(Implicit, Persistent, RoleManager, Item):
    
    def __init__(self,sessionId):
        self._sessionId = sessionId
        self._questionId = OOBTree()
        self._answer = OOBTree()
        self._nav = OOBTree()
        self._context = OOBTree()
        self._loginStatus = OOBTree()
        self._page = OOBTree()
        self._query = OOBTree()
        self._questionContextSet = OOTreeSet()
        
    def addAnswer(self, questionId, answer, nav, time, context, loginStatus, page, query):
        if not self._questionId.has_key(time):
            self._questionId[time] = questionId
            self._answer[time] = answer
            self._nav[time] = nav
            self._context[time] = context
            self._loginStatus[time] = loginStatus
            self._page[time] = page
            self._query[time] = query
            if not self._questionContextSet.has_key([context,questionId]):
                self._questionContextSet.insert([context,questionId])
            return True
        return False
    
    def getTotFeedback(self):
        return len(self._questionId)
    
    #note: isAnswered(questionId, sessionId=sessionId, context=context)
    def isAnswered(self,questionId,**kwargs):
        if len(kwargs) is 1:
            if questionId in self._questionId.values():
                return True
        elif len(kwargs) is 2:
            context = kwargs['context']
            if self._questionContextSet.has_key([context,questionId]):
                return True
        return False
    
    