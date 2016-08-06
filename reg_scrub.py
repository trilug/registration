import html
import member
import re

_allowed_fields = member.ordered_field_names()
_allowed_fields.extend(('del', 'mod', 'reg'))

_bad_requests = []

def sanitize(web_form):
    '''Take a cgi.FieldStorage object and scrub it down to sane values.
    returns a dict with the cgi vars as keys and their html.escape()ed
    values as the values.'''

    # TODO: collect all vars for a given reqid - if the full set's vars
    # don't pass muster, drop that reqid entirely.
    clean_vars = {}
    for var in web_form:
        if name_ok(var):
            if val_ok(web_form[var].value):
                clean_vars[var] = html.escape(web_form[var].value)
    return clean_vars

def name_ok(name):
    '''Check that this is a legal name for a variable in the form.
    The name part must be one of the fields from above, and the reqid
    must consist of only digits.'''
    varparts = name.split('_')
    if len(varparts) == 2:
        if not re.search(r'\D', varparts[1]):
            if varparts[0] in _allowed_fields:
                return True
    return False

def val_ok(string):
    '''Check that this is a valid value from the form.'''

    # If any character besides those listed in the character class below
    # are in the string, then we call shenanigans.  Otherwise, we'll say
    # it's legal.
    if not re.search(r'[^-a-zA-Z0-9_.@# \']', string):
        return True
    return False
