from nap.consent import _
from zope.interface import Interface

from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item


class QType:
    likert_1 = 0        #likert question with answers between a and b
    likert_2 = 1        #likert question with answers between a and b, and not available option
    multi = 2           #multiple choice question
    text = 3            #question needing text answer
    multi_w_text = 4    #multiple choice question with text field for other answer

class Activity:
    browse = 0          #question appears in browsing activity
    search = 1          #question appears in searching activity
    neutral = 3         #question appears in browse activity


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
        if qType in [QType.multi, QType.multi_w_text]:
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
        likertScale = ('1','2','3','4','5')
        if self._type in [QType.likert_1, QType.likert_2]:
            return likertScale
        if self._type in [QType.multi, QType.multi_w_text]:
            return self._choices
        return self._choices
