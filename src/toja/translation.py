TRANSLATIONS = {
    '': 'Unknown',

    # Languages
    'en': 'English',
    'de': 'German',

    # Source types
    'newspaper': 'Newspaper',
    'book': 'Book',

    # Joke types
    'pun': 'Pun',
    'dialogue': 'Dialogue',
    'story': 'Story',
    'wit-wisdom': 'Wit & Wisdom',
    'conundrum': 'Conundrum',
    'verse': 'Verse',
    'definition': 'Definition',
    'factoid': 'Factoid',

    # Person types
    'baby': 'Baby',
    'child': 'Child',
    'adult': 'Adult',
    'elderly': 'Elderly',

    # Gender types
    'female': 'Female',
    'male': 'Male',
    'nonbinary': 'Nonbinary',

    # Class types
    'working': 'Working Class',
    'middle': 'Middle Class',
    'upper': 'Upper Class',
}


def translate(request, key):
    """Translate the given ``key``. Currently is a pure-English dictionary lookup."""
    if isinstance(key, list):
        return [translate(request, value) for value in key]
    elif key in TRANSLATIONS:
        return TRANSLATIONS[key]
    else:
        return key


_ = translate


def includeme(config):
    config.get_jinja2_environment().filters['_'] = translate
