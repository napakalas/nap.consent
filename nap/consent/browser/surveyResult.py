from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from ..tool import Tools
import csv
from StringIO  import StringIO

class SurveyResultView(BrowserView):

    def cleanUp(self):
        if "clearall" in self.request.form:
            Tools.survey.cleanUp()
                
    def getSummary(self):
        survey = Tools.survey
        return survey.getSummary()
    
    def getDownloadLink(self):
        return str(self.context.absolute_url()) + '/survey_csv'

class SurveyCsv(BrowserView):
    def __call__(self):
        out = StringIO()
        writer = csv.writer(out)
        
        answerList = Tools.survey.getAnswerList()
        writer.writerow(['user', 'session', 'timestamp', 'question', 'answer', 'nav', 'context', 'login', 'url', 'search text'])
        for answer in answerList:
            writer.writerow(answer)   
        
        filename = "feedback.csv"
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % filename)
        return out.getvalue()
    