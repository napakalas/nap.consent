from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from ..tool import Tools
import csv
from StringIO  import StringIO

class SurveyResultView(BrowserView):

    def update(self):
        if "clearAll" in self.request.form:
            survey = Tools.survey
            survey.cleanUp()
                
    def getSummary(self):
        survey = Tools.survey
        return survey.getSummary()
    
    def getDownloadLink(self):
        return str(self.context.absolute_url()) + '/survey_csv'

class SurveyCsv(BrowserView):
    def __call__(self):
        out = StringIO()
        writer = csv.writer(out)
    
        writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        
        filename = "feedback.csv"
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % filename)
        return out.getvalue()