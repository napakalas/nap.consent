from zope.annotation.interfaces import IAnnotations
from .content.survey import Survey
from .content.question import QType
from plone import api

class Tools:
    survey = Survey()
    
    @staticmethod
    def initSurvey():
        if Tools.survey is None:
            Tools.survey = Survey()
        if Tools.survey.getQuestionTot() > 0:
            return Tools.survey
        #QType: likert_1, likert_2, multi, text
        # multi: *args = choices
        # likert_1, likert_2: *args = q_Low, q_High
        Tools.survey.addQuestion(QType.likert_1, 'How familiar are you with this website?', 'not familiar', 'very familiar')
        Tools.survey.addQuestion(QType.multi, 'How often do you usually access this website in a month?', '< 5 times', '5 - 10 times', '11 - 20 times', '> 20 times')
        Tools.survey.addQuestion(QType.likert_2, 'How familiar you are with the topic you are looking for?', 'not familiar', 'very familiar')
        Tools.survey.addQuestion(QType.likert_2, 'In what level, you need a snippet for each model?', 'i do not need it', 'i really need it')
        Tools.survey.addQuestion(QType.text, 'What kind of information do you required presented by a snippet?')
        Tools.survey.addQuestion(QType.likert_1, 'In what level, a query suggestion features is useful for you?', 'not useful', 'very useful')
        Tools.survey.addQuestion(QType.likert_2, 'In what level, you are satisfied with the results list?', 'not satisfy', 'very satisfy')
        Tools.survey.addQuestion(QType.text, 'Please provide suggestions to improve the presentation of this result list?')
        Tools.survey.addQuestion(QType.text, 'Thanks for your feedback. What could we do to improve?')
        Tools.survey.addQuestion(QType.multi, 'Regarding your information needs, which link on this page is the most suitable for you?', 'documentation', 'model metadata', 'model curation', 'mathematics', 'generated code', 'cite this model', 'source view', 'other')
        Tools.survey.addQuestion(QType.multi, 'Regarding your information needs, which part on this page is the most suitable for you?', 'model status', 'model structure', 'schematic diagram', 'original paper', 'reference', 'other')
        Tools.survey.addQuestion(QType.likert_2, 'How relevant is this page to the information you are looking for?', 'not satisfy', 'very satisfy')
        Tools.survey.addQuestion(QType.likert_2, 'If this is the page you are looking for, how fast can you get this page?', 'very slow', 'very vast')
        Tools.survey.addQuestion(QType.likert_2, 'If this is the page you are looking for, how easy do you get this page?', 'very difficult', 'very easy')
        Tools.survey.addQuestion(QType.likert_2, 'How easy is it to get your intended information?', 'very difficult', 'very easy')
        Tools.survey.addQuestion(QType.likert_2, 'If you are looking for information using browse facility and if this is the page you are looking for, how easy is it to find information with browsing facilities compared to search facilities?', 'very difficult', 'very easy')
        return Tools.survey
        
    @staticmethod
    def getRootAnn():
        portal = api.portal.get()
        annotations = IAnnotations(portal)
        return annotations
    