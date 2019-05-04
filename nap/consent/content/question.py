from nap.consent import _
from zope.interface import Interface
from zope.interface import implements

from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item


class QType:
    likert_1 = 1
    likert_2 = 2
    multi = 3
    text = 4

class IQuestion(Interface):
    """A question for PMR."""

class Question(Implicit, Persistent, RoleManager, Item):
    implements(IQuestion)
    
    # multi: *args = choices
    # likert_1, likert_2: *args = q_Low than q_High
    def __init__(self, q_Id, q_Type, q_Question, *args):
        self.__id = q_Id
        self.__type = q_Type
        self.__question = q_Question
        if q_Type is QType.likert_1 or q_Type is QType.likert_2:
            self.__low = args[0]
            self.__high = args[1]
        else:
            self.__low = None
            self.__high = None
        if q_Type is QType.multi:
            self.__choices = args
        else:
            self.__choices = None
        
    def getId(self):
        return self.__id
    
    def getType(self):
        return self.__type
    
    def getQuestionText(self):
        return self.__question
    
    def getLow(self):
        return self.__low
    
    def getHigh(self):
        return self.__high
    
    def getChoices(self):
        if self.__type is QType.likert_1:
            return (0,1,2,3,4)
        if self.__type is QType.likert_2:
            return (0,1,2,3,4,5)
        if self.__type is QType.multi:
            return self.__choices
        return self.__choices


    