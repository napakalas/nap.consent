from zope.annotation.interfaces import IAnnotations
from .content.survey import Survey
from .content.question import QType as qt
from .content.question import Activity as act
from plone import api
from .content.survey import PType as pt
from .content.survey import Appear as ap

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

        #id=0
        Tools.survey.addQuestion(qt.text, 'Thanks for your feedback. What else can we do to improve your PMR experience?', act.neutral, None)
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.allpages)

        #id=1
        Tools.survey.addQuestion(qt.multi, 'How often do you usually access the PMR?', act.neutral, None, 'On a daily basis', 'Several times every week', 'Several times each month', 'Several times a year', 'First time user or very rarely')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.general)

        #id=2
        Tools.survey.addQuestion(qt.likert_1, 'I have a particular biomedical domain of interest (e.g. cardiovascular, gastrointestinal, immunology, etc).', act.neutral, None, 'no interest', 'strong interest')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search,pt.browse)

        #id=3
        Tools.survey.addQuestion(qt.likert_1, 'I have a particular biophysical mechanism of interest (e.g. electrophysiology, ion transport, gene regulation, etc).', act.neutral, None, 'no interest', 'strong interest')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search,pt.browse)

        #id=4
        Tools.survey.addQuestion(qt.likert_2, 'A concise informative snippet is needed for each model presented in the result list.', act.neutral, None, 'strongly disagree', 'strongly agree')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        #id=5
#        parent = Tools.survey.getLastQuestionId()
        Tools.survey.addQuestion(qt.multi_w_text, 'What kind of information do you require to be presented by a snippet?', act.neutral, None, 'biomedical domain', 'biophysical mechanism', 'anatomical location', 'species', 'tissue', 'scale', 'type of maths', 'other (specify)')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        #id=6
        Tools.survey.addQuestion(qt.likert_1, 'How important a query suggestion feature will be for you?', act.neutral, None, 'not useful at all', 'extremely useful')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        #id=7
        Tools.survey.addQuestion(qt.likert_2, 'How satisfied are you with the content of the results list?', act.neutral, None, 'not satisfied at all', 'extremely satisfied')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search)

        #id=8
        Tools.survey.addQuestion(qt.likert_2, 'How satisfied are you with the presentation of the results list?', act.neutral, None, 'not satisfied at all', 'extremely satisfied')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search)

        #id=9
        Tools.survey.addQuestion(qt.multi_w_text, 'Regarding your information needs which link on this page is the most suitable for you?', act.neutral, None, 'documentation', 'model metadata', 'model curation', 'mathematics', 'generated code', 'cite this model', 'source view', 'other (specify)')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.file)

        #id=10
        Tools.survey.addQuestion(qt.multi_w_text, 'Regarding your information needs which part on this page is the most suitable for you?', act.neutral, None, 'model status', 'model structure', 'schematic diagram', 'original paper', 'reference', 'other (specify)')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.document,pt.file)

        #id=11
        Tools.survey.addQuestion(qt.likert_2, 'How relevant are the results to the information you are looking for?', act.search, None, 'not relevant at all', 'extremely relevant')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        #id=12
        Tools.survey.addQuestion(qt.likert_2, 'If this is the page you are looking for how fast can you get this page?', act.search, None, 'extremely slow', 'extremely fast')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        #id=13
        Tools.survey.addQuestion(qt.likert_2, 'If this is the page you are looking for how easy/intuitive was it to get to this page?', act.search, None, 'extremely difficult', 'extremely easy')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        #id=14
        Tools.survey.addQuestion(qt.likert_2, 'If you used the browse feature instead of searching how easy was is it to find information you were looking?', act.browse, None, 'extremely difficult', 'extremely easy')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        return Tools.survey
