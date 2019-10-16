from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from ..tool import Tools
import csv
from StringIO import StringIO
from plone import api
import hashlib

def isAuthorised(text):
    coder = hashlib.md5()
    coder.update(text.encode("utf-8"))
    encode = coder.hexdigest()
    if encode in ['45afef383e7a96c833201d718235c70c', '7a9640959c14018ea824487e8f735ae4'] or 'Manager' in api.user.get_roles(user=api.user.get_current()):
        return True
    else:
        return False

class SurveyResultView(BrowserView):
    def cleanUp(self):
        if not api.user.is_anonymous():
            if "clearall" in self.request.form:
                if isAuthorised(self.request.form['passwdDelete']):
                    totDelete = Tools.survey.cleanUp()
                    return "Deleted user: " + str(totDelete)
                else:
                    return "Deleted user: 0"
        else:
            return "You do not have permissions to delete data"

    def getSummary(self):
        survey = Tools.survey
        return survey.getSummary()

    def getDownloadLink(self):
        if api.user.is_anonymous():
            return ''
        else:
            link = "downloadAll('" + str(self.context.absolute_url()
                                         ) + '/survey_csv' + "')"
            return link

    def isDeletable(self):
        if not api.user.is_anonymous():
            return True
        return False


class SurveyCsv(BrowserView):
    def __call__(self):
        if not api.user.is_anonymous():
            if isAuthorised(self.request.form['passwd']):
                out = StringIO()
                writer = csv.writer(out)
                answerList = Tools.survey.getAnswerList()
                writer.writerow(['user', 'session', 'timestamp', 'question',
                                 'answer', 'nav', 'context', 'login', 'url', 'search text'])
                for answer in answerList:
                    writer.writerow(answer)
                filename = "feedback.csv"
                self.request.response.setHeader('Content-Type', 'text/csv')
                self.request.response.setHeader(
                    'Content-Disposition', 'attachment; filename="%s"' % filename)
                return out.getvalue()
            else:
                return ""
        else:
            return "You do not have permissions to download"
