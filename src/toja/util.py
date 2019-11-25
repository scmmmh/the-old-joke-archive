import cerberus
import logging
import smtplib

from cgi import FieldStorage
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formatdate
from jinja2 import Undefined


def convert_type(value, target_type, default=None):
    """Attempts to convert the ``value`` to the given ``target_type``. Will
    return ``default`` if the conversion fails.

    Supported ``target_type`` values are:

    * `int` -- Convert to an integer value
    * `boolean` -- Convert to a boolean value (``True`` if the value is the
      ``unicode`` string "true" in any capitalisation
    * `list` -- Convert to a list, splitting on line-breaks and commas

    :param value: The value to convert
    :type value: `unicode`
    :param target_type: The target type to convert to
    :type target_type: `unicode`
    :param default: The default value if the conversion fails
    :return: The converted value
    """
    if target_type == 'int':
        try:
            return int(value)
        except ValueError:
            return default
    elif target_type == 'boolean':
        if value and value.lower() == 'true':
            return True
        else:
            return False
    elif target_type == 'list':
        return [v.strip() for line in value.split('\n') for v in line.split(',') if v.strip()]
    if value:
        return value
    else:
        return default


# Cached application settings for faster access
CACHED_SETTINGS = {}


def get_config_setting(request, key, target_type=None, default=None):
    """Gets a configuration setting from the application configuration.
    Settings are cached for faster access.

    :param request: The request used to access the configuration settings
    :type request: :class:`~pyramid.request.Request`
    :param key: The configuration key
    :type key: `unicode`
    :param target_type: If specified, will convert the configuration setting
                        to the given type using :func:`~toja.util.convert_type`
    :type default: The default value to return if there is no setting with the
                   given key
    :return: The configuration setting value or ``default``
    """
    global CACHED_SETTINGS
    if key in CACHED_SETTINGS:
        return CACHED_SETTINGS[key]
    else:
        if key in request.registry.settings:
            if target_type:
                CACHED_SETTINGS[key] = convert_type(request.registry.settings[key], target_type, default=default)
            else:
                CACHED_SETTINGS[key] = request.registry.settings[key]
        else:
            CACHED_SETTINGS[key] = default
        return get_config_setting(request, key, target_type=target_type, default=default)


def send_email(request, recipient, sender, subject, text):  # pragma: no cover
    """Sends an e-mail based on the settings in the configuration file. If
    the configuration does not have e-mail settings or if there is an
    exception sending the e-mail, then it will log an error.

    :param request: The current request used to access the settings
    :type request: :class:`pyramid.request.Request`
    :param recipient: The recipient's e-mail address
    :type recipient: `unicode`
    :param sender: The sender's e-mail address
    :type sender: `unicode`
    :param subject: The e-mail's subject line
    :type subject: `unicode`
    :param text: The e-mail's text body content
    :type text: `unicode`
    """
    if get_config_setting(request, 'app.email.smtp_host'):
        email = MIMEText(text)
        email['Subject'] = subject
        email['From'] = sender
        email['To'] = recipient
        email['Date'] = formatdate()
        try:
            smtp = smtplib.SMTP(get_config_setting(request, 'app.email.smtp_host'))
            if get_config_setting(request, 'app.email.ssl', target_type='bool', default=False):
                smtp.starttls()
            username = get_config_setting(request, 'app.email.username')
            password = get_config_setting(request, 'app.email.password')
            if username and password:
                smtp.login(username, password)
            smtp.sendmail(sender, recipient, email.as_string())
            smtp.quit()
        except Exception as e:
            logging.getLogger("toja").error(str(e))
            print(text)  # noqa TODO: Remove
    else:
        logging.getLogger("toja").error('Could not send e-mail as "app.email.smtp_host" setting not specified')
        print(text)  # noqa TODO: Remove


fieldstorage_type = cerberus.TypeDefinition('fieldstorage', (FieldStorage,), ())


class Validator(cerberus.Validator):
    """Extended Validator that can check whether two fields match."""

    types_mapping = cerberus.Validator.types_mapping.copy()
    types_mapping['fieldstorage'] = fieldstorage_type

    def _validate_matches(self, other, field, value):
        if other not in self.document:
            self._error(field, 'You must provide a value.')
        if self.document[other] != value:
            self._error(field, 'The value does not match.')


def date_to_json(date):
    """Converts a date into ISO-XXX representation for use in JSON data."""
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


MONTHS = {1: 'January',
          2: 'February',
          3: 'March',
          4: 'April',
          5: 'May',
          6: 'June',
          7: 'July',
          8: 'August',
          9: 'September',
          10: 'October',
          11: 'November',
          12: 'December'}


def fancy_date(value, format='long'):
    """Generate a fancy date string. Handles both :class:`~datetime.datetime` objects and potentially partial
    YYYY-MM-DD string values. The format is one of:

    * long - Month day in the year (with fallbacks for missing data)
    * year - Just a year
    * month - Just a month as the month name
    * day - Just the day of the month with suffix
    * any combination of the last three separated by ``'-'``, with an optional `'`?`'` prefix to optional parts."""
    if format == 'long':
        if isinstance(value, datetime):
            day = fancy_date(value, format='day')
            month = fancy_date(value, format='month')
            year = fancy_date(value, format='year')
            if year:
                if month:
                    if day:
                        return '{0} {1} in the year {2}'.format(month, day, year)
                    else:
                        return '{0} in the year {1}'.format(month, year)
                else:
                    return year
            return Undefined(format='long')
        else:
            pass
    elif format == 'year':
        if isinstance(value, datetime):
            return value.year
        else:
            value = value.split('-')
            if len(value) >= 1:
                return int(value[0])
        return Undefined(name='year')
    elif format == 'month':
        month = Undefined(name='month')
        if isinstance(value, datetime):
            month = value.month
        else:
            value = value.split('-')
            if len(value) >= 2:
                month = int(value[1])
        if month:
            return MONTHS[month]
        return month
    elif format == 'day':
        day = Undefined(name='day')
        if isinstance(value, datetime):
            day = value.day
        else:
            value = value.split('-')
            if len(value) == 3:
                day = int(value[2])
        if day:
            if day in [1, 21, 31]:
                return '{0}st'.format(day)
            elif day in [2, 22]:
                return '{0}nd'.format(day)
            elif day == 3:
                return '{0}rd'.format(day)
            else:
                return '{0}th'.format(day)
        return day
    else:
        format = format.split('-')
        result = []
        for part in format:
            if part.startswith('?'):
                part_value = fancy_date(value, part[1:])
            else:
                part_value = fancy_date(value, part)
            if part_value:
                result.append(part_value)
            elif not part.startswith('?'):
                return Undefined(name=format)
        return ' '.join(result)


def strftime(value, format):
    """Apply a stftime format to a date value."""
    return value.strftime(format)


def includeme(config):
    config.get_jinja2_environment().filters['config'] = get_config_setting
    config.get_jinja2_environment().filters['zip'] = zip
    config.get_jinja2_environment().filters['fancy_date'] = fancy_date
    config.get_jinja2_environment().filters['strftime'] = strftime
