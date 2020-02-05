from jinja2 import Undefined

SOURCE_METADATA = [{'name': 'pub_type',
                    'type': 'select',
                    'values': ['newspaper', 'book'],
                    'label': 'Publication Type'},
                   {'name': 'pub_title', 'type': 'text', 'label': 'Publication Title'},
                   {'name': 'pub_date', 'type': 'date', 'label': 'Publication Date'},
                   {'name': 'pub_location', 'type': 'text', 'label': 'Publication Location'},
                   {'name': 'pub_section', 'type': 'text', 'label': 'Column / Chapter Title'},
                   {'name': 'pub_page_numbers', 'type': 'text', 'label': 'Page Numbers'},
                   {'name': 'pub_publisher', 'type': 'text', 'label': 'Publisher'},
                   ]
SOURCE_SNIPPET_FIELD_TITLE = 'pub_title'
SOURCE_SNIPPET_FIELD_SUBTITLE = 'pub_section'
SOURCE_SNIPPET_FIELD_DATE = 'pub_date'
ANNOTATIONS = [{'name': 'title', 'label': 'Title'},
               {'name': 'attribution', 'label': 'Attribution'},
               {'name': 'aside', 'label': 'Aside'},
               {'name': 'person',
                'label': 'Person',
                'attrs': [{'name': 'age',
                           'label': 'Age',
                           'type': 'select',
                           'values': ['', 'baby', 'child', 'adult', 'elderly']},
                          {'name': 'gender',
                           'label': 'Gender',
                           'type': 'select',
                           'values': ['', 'female', 'male', 'nonbinary']},
                          {'name': 'class',
                           'label': 'Social Status',
                           'type': 'select',
                           'values': ['', 'working', 'middle', 'upper']}
                          ],
                'separate': True},
               {'name': 'location', 'label': 'Location'},
               {'name': 'object', 'label': 'Object'},
               {'name': 'speech', 'label': 'Speech', 'separate': True},
               {'name': 'question', 'label': 'Question', 'separate': True},
               {'name': 'answer', 'label': 'Answer'},
               ]
JOKE_TYPES = ['pun', 'dialogue', 'story', 'wit-wisdom', 'conundrum', 'verse', 'definition', 'factoid']
JOKE_METADATA = [{'name': 'type',
                  'label': 'Type of Joke',
                  'type': 'multichoice',
                  'values': JOKE_TYPES},
                 {'name': 'language',
                  'label': 'Language',
                  'type': 'select',
                  'values': ['', 'en', 'de']},
                 {'name': 'title',
                  'label': 'Title',
                  'type': 'extract-single',
                  'source': {'type': 'title',
                             'attr': 'text'}},
                 ]
SEARCH_FACETS = [{'name': 'type', 'type': 'text', 'label': 'Joke Type'},
                 {'name': 'language', 'type': 'text', 'label': 'Language'},
                 {'name': 'pub_type', 'type': 'text', 'label': 'Publication Type'},
                 {'name': 'pub_title', 'type': 'text', 'label': 'Publication'},
                 {'name': 'pub_section', 'type': 'text', 'label': 'Publication Section'},
                 {'name': 'pub_date', 'type': 'date', 'label': 'Publication Date'},
                 ]
SEARCH_FACET_FIELD_NAMES = [facet['name'] for facet in SEARCH_FACETS]

SETTINGS = {'SOURCE_METADATA': SOURCE_METADATA,
            'SOURCE_SNIPPET_FIELD_TITLE': SOURCE_SNIPPET_FIELD_TITLE,
            'SOURCE_SNIPPET_FIELD_SUBTITLE': SOURCE_SNIPPET_FIELD_SUBTITLE,
            'SOURCE_SNIPPET_FIELD_DATE': SOURCE_SNIPPET_FIELD_DATE,
            'ANNOTATIONS': ANNOTATIONS,
            'SEARCH_FACETS': SEARCH_FACETS,
            'SEARCH_FACET_FIELD_NAMES': SEARCH_FACET_FIELD_NAMES,
            'JOKE_TYPES': JOKE_TYPES,
            'JOKE_METADATA': JOKE_METADATA,
            }


def get_setting(request, setting):
    """Get a configuration setting."""
    if setting in SETTINGS:
        return SETTINGS[setting]
    else:
        return Undefined(name=setting)


def includeme(config):
    config.get_jinja2_environment().filters['setting'] = get_setting
