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
        self._qstPage = OOTreeSet()

    def addAnswer(self, questionId, answer, nav, time, context, loginStatus, page, query):
        if not self._questionId.has_key(time):
            self._questionId[time] = questionId
            self._answer[time] = answer
            self._nav[time] = nav
            self._context[time] = context
            self._loginStatus[time] = loginStatus
            self._page[time] = page
            self._query[time] = query
            self._qstPage.insert(str(questionId)+str(page))
            return True
        return False

    def getTotFeedback(self):
        return len(self._questionId)

    #note: isAnswered(questionId, sessionId=sessionId, page=url)
    def isAnswered(self,questionId,**kwargs):
        if 'page' in kwargs:
            qstPage = str(questionId)+str(kwargs['page'])
            return True if self._qstPage.has_key(qstPage) else False
        else:
            return True if questionId in self._questionId.values() else False

    def getAnswerList(self):
        answers = []
        for time in self._questionId.keys():
            tmp = [self._sessionId, time, self._questionId.get(time), self._answer.get(time), self._nav.get(time), self._context.get(time), self._loginStatus.get(time), self._page.get(time), self._query.get(time)]
            answers.append(tmp)
        return answers
