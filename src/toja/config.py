from jinja2 import Undefined

SOURCE_METADATA = [{'name': 'pub_type',
                    'type': 'select',
                    'values': [('newspaper', 'Newspaper'),
                               ('book', 'Book')],
                    'label': 'Publication Type'},
                   {'name': 'pub_title', 'type': 'text', 'label': 'Publication Title'},
                   {'name': 'pub_date', 'type': 'date', 'label': 'Publication Date (YYYY-MM-DD, YYYY-MM, or YYYY)'},
                   {'name': 'pub_location', 'type': 'text', 'label': 'Publication Location'},
                   {'name': 'pub_section', 'type': 'text', 'label': 'Column / Chapter Title'},
                   {'name': 'pub_page_numbers', 'type': 'text', 'label': 'Page Numbers'},
                   {'name': 'pub_publisher', 'type': 'text', 'label': 'Publisher'},
                   ]
SOURCE_SNIPPET_FIELD_TITLE = 'pub_title'
SOURCE_SNIPPET_FIELD_SUBTITLE = 'pub_section'
SOURCE_SNIPPET_FIELD_DATE = 'pub_date'
JOKE_SNIPPET_FIELD_TITLE = 'source.pub_title'
JOKE_SNIPPET_FIELD_SUBTITLE = 'source.pub_section'
JOKE_SNIPPET_FIELD_DATE = 'pub_date'
ANNOTATIONS = [{'name': 'title', 'label': 'Title'},
               {'name': 'attribution', 'label': 'Attribution'},
               {'name': 'person', 'label': 'Person'},
               {'name': 'speaker', 'label': 'Speaker'},  # TODO: Remove
               {'name': 'speech', 'label': 'Speech'},
               {'name': 'aside', 'label': 'Aside'},
               {'name': 'question', 'label': 'Question'},
               {'name': 'answer', 'label': 'Answer'},
               {'name': 'location', 'label': 'Location'},
               {'name': 'object', 'label': 'Object'},
               ]
JOKE_TYPES = [{'name': 'pun', 'label': 'Pun'},
              {'name': 'dialogue', 'label': 'Dialogue'},
              {'name': 'story', 'label': 'Story'},
              {'name': 'wit-wisdom', 'label': 'Wit & Wisdom'},
              {'name': 'conundrum', 'label': 'Conundrum'},
              {'name': 'verse', 'label': 'Verse'},
              {'name': 'definition', 'label': 'Definition'},
              {'name': 'factoid', 'label': 'Factoid'},
              ]
JOKE_METADATA = [{'name': 'type',
                  'label': 'Type of Joke',
                  'type': 'multichoice',
                  'values': JOKE_TYPES},
                 {'name': 'language',
                  'label': 'Language',
                  'type': 'select',
                  'values': [{'name': 'en', 'label': 'English'}]},
                 ]
SEARCH_FACETS = [{'name': 'pub_title', 'type': 'text', 'label': 'Publication'},
                 {'name': 'pub_section', 'type': 'text', 'label': 'Section'},
                 {'name': 'pub_date', 'type': 'date', 'label': 'Date'}]

SETTINGS = {'SOURCE_METADATA': SOURCE_METADATA,
            'SOURCE_SNIPPET_FIELD_TITLE': SOURCE_SNIPPET_FIELD_TITLE,
            'SOURCE_SNIPPET_FIELD_SUBTITLE': SOURCE_SNIPPET_FIELD_SUBTITLE,
            'SOURCE_SNIPPET_FIELD_DATE': SOURCE_SNIPPET_FIELD_DATE,
            'JOKE_SNIPPET_FIELD_TITLE': JOKE_SNIPPET_FIELD_TITLE,
            'JOKE_SNIPPET_FIELD_SUBTITLE': JOKE_SNIPPET_FIELD_SUBTITLE,
            'JOKE_SNIPPET_FIELD_DATE': JOKE_SNIPPET_FIELD_DATE,
            'ANNOTATIONS': ANNOTATIONS,
            'SEARCH_FACETS': SEARCH_FACETS,
            'JOKE_TYPES': JOKE_TYPES,
            }


def get_setting(request, setting):
    """Get a configuration setting."""
    if setting in SETTINGS:
        return SETTINGS[setting]
    else:
        return Undefined(name=setting)


def includeme(config):
    config.get_jinja2_environment().filters['setting'] = get_setting
