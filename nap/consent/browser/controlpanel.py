from nap.consent import _
from nap.consent.config import IS_BBB
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface
from zope.interface import provider
from zope.interface import invariant
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.i18n import translate
from zope.globalrequest import getRequest
from plone.autoform import directives as form
from time import time
from plone.supermodel import model

DEFAULT_CONSENT = (
    u'<p>We are now working on the Smart searching for the Physiome Project. '
    u'This project aim is to easy research communities when looking for relevant knowledge on this website. '
    u'Therefore, we need your help by allowing cookies '
    u'and answering short questions. '    
    u'We use cookies for statistical purposes, '
    u'to make select questions, '
    u'to analyse your effort, '
    u'or to remember your settings. '
    u'Click the button for more info.</p>')

class IBrowserLayer(Interface):
    """A layer specific for this add-on product."""
    
@provider(IContextAwareDefaultFactory)
def default_title(context):
    # we need to pass the request as translation context
    return translate(
        _('default_title', default=u'We need your help'),
        context=getRequest())


@provider(IContextAwareDefaultFactory)
def default_text(context):
    # we need to pass the request as translation context
    return translate(
        _('default_text', default=DEFAULT_CONSENT),
        context=getRequest())

class IConsentControlPanel(model.Schema):
    
    enabled = schema.Bool(
        title=_(u'title_enabled', default=u'Allow consent?'),
        description=_(
            u'help_enabled',
            default=u'Show a consent form for survey first time accessing'),
        default=False,
        required=False,
    )
    
    title = schema.TextLine(
        title=_(u'title_title', default=u'Title'),
        description=_(u'help_title', default=u'A title for the consent.'),
        required=False,
        defaultFactory=default_title,
    )
    
    # XXX: we must use Text instead of RichText as we can only store
    #      primitive Python data types in plone.app.registry
    #      see: https://community.plone.org/t/1240
    if IS_BBB:
        # BBB: remove on deprecation of Plone 4.3
        from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
        form.widget('text', WysiwygFieldWidget)
    else:
        form.widget('text', klass='pat-tinymce')
    text = schema.Text(
        title=_(u'title_text', default=u'Body text'),
        description=_(u'help_text', default=u'The text of the disclaimer.'),
        required=True,
        defaultFactory=default_text,
    )
    
    deleteData = schema.Bool(
        title=_(u'title_enabled', default=u'Finish the survey? Do not need the data anymore'),
        description=_(
            u'help_enabled',
            default=u'Make sure you have backed up the data before activating this choice. The deleted data is not recoverable'),
        default=False,
        required=False,
    )


class ConsentControlPanelForm(RegistryEditForm):
    schema = IConsentControlPanel
    label = _(u'Consent Settings')
    description = _(u'Show a consent the first time a user visits a site.')

class ConsentControlPanelView(ControlPanelFormWrapper):
    """Control panel form wrapper."""
    form = ConsentControlPanelForm
    