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

class User(Implicit, Persistent, RoleManager, Item):
    def __init__(self,username):
        self._username = username
        
    