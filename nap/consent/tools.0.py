from zope.annotation.interfaces import IAnnotations
#from .content.survey import Survey
#from .content.question import QType



#survey = Survey()

#def getSurvey():
#    global survey
#    if survey is None:
#        survey = Survey()
#    return survey

#def deleteSurvey():
#    global survey
#    if survey is not None:
#        del survey
#        survey = Survey()

def getQuestionType(context):
    annotations = IAnnotations(context)
    return annotations
    
#QType:
    #likert_1
    #likert_2
    #multi
    #text
# multi: *args = choices
# likert_1, likert_2: *args = q_Low, q_High
#survey.addQuestion(QType.likert_1, 'How familiar are you with this website?', 'not familiar', 'very familiar')
#survey.addQuestion(QType.multi, 'How often do you usually access this website in a month?', '< 5 times', '5 - 10 times', '11 - 20 times', '> 20 times')
#survey.addQuestion(QType.likert_2, 'How familiar you are with the topic you are looking for?', 'not familiar', 'very familiar')
#survey.addQuestion(QType.likert_2, 'In what level, you need a snippet for each model?', 'i don’t need it', 'i really need it')
#survey.addQuestion(QType.text, 'What kind of information do you required presented by a snippet?')
#survey.addQuestion(QType.likert_1, 'In what level, a query suggestion features is useful for you?', 'not useful', 'very useful')
#survey.addQuestion(QType.likert_2, 'In what level, you are satisfied with the results list?', 'not satisfy', 'very satisfy')
#survey.addQuestion(QType.text, 'Please provide suggestions to improve the presentation of this result list?')
#survey.addQuestion(QType.text, 'Thanks for your feedback. What could we do to improve?')
#survey.addQuestion(QType.multi, 'Regarding your information needs, which link on this page is the most suitable for you?', 'documentation', 'model metadata', 'model curation', 'mathematics', 'generated code', 'cite this model', 'source view', 'other')
#survey.addQuestion(QType.multi, 'Regarding your information needs, which part on this page is the most suitable for you?', 'model status', 'model structure', 'schematic diagram', 'original paper', 'reference', 'other')
#survey.addQuestion(QType.likert_2, 'How relevant is this page to the information you are looking for?', 'not satisfy', 'very satisfy')
#survey.addQuestion(QType.likert_2, 'If this is the page you are looking for, how fast can you get this page?', 'not slow', 'very vast')
#survey.addQuestion(QType.likert_2, 'If this is the page you are looking for, how easy do you get this page?', 'not difficult', 'very easy')
#survey.addQuestion(QType.likert_2, 'How easy is it to get your intended information?', 'not difficult', 'very easy')
#survey.addQuestion(QType.likert_2, 'If you are looking for information using browse facility and if this is the page you are looking for, how easy is it to find information with browsing facilities compared to search facilities?', 'not difficult', 'very easy')


#def setupAnnotations(context):
#    """
#    set up the annotations if they haven't been set up
#    already. The rest of the functions in here assume that
#    this has already been set up
#    """
#    annotations = IAnnotations(context)

#    if name not in annotations:
#        annotations[name] = Survey()
#    return annotations

#never call it
#def clearAnnotations(context):
#    ann = IAnnotations()
#    for key in list(ann.keys()): # Little destructive here, deletes *all* annotations
#        del ann[key]