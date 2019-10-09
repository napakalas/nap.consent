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
        Tools.survey.addQuestion(qt.text, 'Thanks for your feedback. What could we do to improve?', act.neutral, None)
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.allpages)

        Tools.survey.addQuestion(qt.likert_1, 'How familiar are you with this website?', act.neutral, None, 'not familiar', 'very familiar')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.general)

        Tools.survey.addQuestion(qt.multi, 'How often do you usually access the PMR?', act.neutral, None, 'On a daily basis', 'Several times every week', 'First time user or very rarely')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.general)

        Tools.survey.addQuestion(qt.likert_2, 'How familiar you are with the topic you are looking for?', act.neutral, None, 'not familiar', 'very familiar')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search,pt.browse)

        Tools.survey.addQuestion(qt.likert_1, 'I have a particular biomedical domain of interest (e.g. cardiovascular, gastrointestinal, immunology, etc)', act.neutral, None, 'no interes', 'strong interest')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search,pt.browse)

        Tools.survey.addQuestion(qt.likert_2, 'In what level, you need a snippet for each model?', act.neutral, None, 'i do not need it', 'i really need it')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        Tools.survey.addQuestion(qt.text, 'What kind of information do you required presented by a snippet?', act.neutral, 4)
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        Tools.survey.addQuestion(qt.likert_1, 'In what level, a query suggestion features is useful for you?', act.neutral, None, 'not useful', 'very useful')
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        Tools.survey.addQuestion(qt.text, 'Please provide suggestions to improve the presentation of this result list?', act.neutral, None)
        Tools.survey.setLastQuestionPages(ap.oneForAll, pt.search)

        Tools.survey.addQuestion(qt.likert_2, 'In what level, you are satisfied with the results list?', act.neutral, None, 'not satisfy', 'very satisfy')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.search)

        Tools.survey.addQuestion(qt.multi, 'Regarding your information needs, which link on this page is the most suitable for you?', act.neutral, None, 'documentation', 'model metadata', 'model curation', 'mathematics', 'generated code', 'cite this model', 'source view', 'other')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.file)

        Tools.survey.addQuestion(qt.multi, 'Regarding your information needs, which part on this page is the most suitable for you?', act.neutral, None, 'model status', 'model structure', 'schematic diagram', 'original paper', 'reference', 'other')
        Tools.survey.setLastQuestionPages(ap.onePerSession, pt.document,pt.file)

        Tools.survey.addQuestion(qt.likert_2, 'How relevant are the results to the information you are looking for?', act.search, None, 'not relevant at all', 'extremely relevant')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        Tools.survey.addQuestion(qt.likert_2, 'If this is the page you are looking for how fast can you get this page?', act.search, None, 'extremely slow', 'extremely fast')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        Tools.survey.addQuestion(qt.likert_2, 'If this is the page you are looking for how easy do you get this page?', act.search, None, 'extremely difficult', 'extremely easy')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        Tools.survey.addQuestion(qt.likert_2, 'How easy is it to get your intended information?', act.search, None, 'very difficult', 'very easy')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        Tools.survey.addQuestion(qt.likert_2, 'If you used the browse feature instead of searching how easy was is it to find information you were looking?', act.browse, None, 'extremely difficult', 'extremely easy')
        Tools.survey.setLastQuestionPages(ap.onePerSessionPage, pt.document,pt.file)

        return Tools.survey