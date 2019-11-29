from jinja2 import Undefined

SOURCE_METADATA = [{'name': 'pub_title', 'type': 'text', 'label': 'Publication'},
                   {'name': 'pub_section', 'type': 'text', 'label': 'Section'},
                   {'name': 'pub_date', 'type': 'date', 'label': 'Date'}]
JOKE_SNIPPET_FIELD_TITLE = 'source.pub_title'
JOKE_SNIPPET_FIELD_SUBTITLE = 'source.pub_section'
JOKE_SNIPPET_FIELD_DATE = 'pub_date'
ANNOTATIONS = [{'name': 'title', 'label': 'Titel'},
               {'name': 'attribution', 'label': 'Attribution'},
               {'name': 'speaker', 'label': 'Speaker'},
               {'name': 'speech', 'label': 'Speech'},
               {'name': 'aside', 'label': 'Aside'},
               {'name': 'question', 'label': 'Question'},
               {'name': 'answer', 'label': 'Answer'}]

SETTINGS = {'SOURCE_METADATA': SOURCE_METADATA,
            'JOKE_SNIPPET_FIELD_TITLE': JOKE_SNIPPET_FIELD_TITLE,
            'JOKE_SNIPPET_FIELD_SUBTITLE': JOKE_SNIPPET_FIELD_SUBTITLE,
            'JOKE_SNIPPET_FIELD_DATE': JOKE_SNIPPET_FIELD_DATE,
            'ANNOTATIONS': ANNOTATIONS}


def get_setting(request, setting):
    """Get a configuration setting."""
    if setting in SETTINGS:
        return SETTINGS[setting]
    else:
        return Undefined(name=setting)


def includeme(config):
    config.get_jinja2_environment().filters['setting'] = get_setting
