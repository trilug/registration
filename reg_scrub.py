import copy
import html
import re
import sys
import time

from member import Member

_actions        = ('del', 'mod', 'reg', 'act')
_allowed_fields = Member.field_names() + _actions

def _print_err(*args, **kwargs):
    print(time.strftime("[%a %b %d %H:%M:%S %Y] ", time.localtime(time.time())), file=sys.stderr, end='')
    print("[{}] ".format(__file__), file=sys.stderr, end='')
    print(*args, file=sys.stderr, **kwargs)

def cleanse_and_validate(web_form):
    cleansed_form = sanitize(web_form)
    for reqid in list(cleansed_form.keys()):
        tmp = copy.deepcopy(cleansed_form[reqid])
        missing_field = False
        for f in _allowed_fields:
            try:
                tmp.pop(f+'_'+reqid)
            except KeyError:
                if f not in _actions and f not in Member.optional_field_names():
                    _print_err("Missing required field: {}".format(f))
                    missing_field = True
        if len(tmp) or missing_field:
            cleansed_form.pop(reqid)
        else:
            tmp = copy.deepcopy(cleansed_form[reqid])
            if 'del_'+reqid in tmp:
                if 'mod_'+reqid in tmp:
                    print("<strong>No action taken on request id {}: ".format(reqid)
                        +"Cannot both modify and cancel a request.</strong></br>")
                    cleansed_form.pop(reqid)
                if 'reg_'+reqid in tmp:
                    print("<strong>No action taken on request id {}: ".format(reqid)
                        +"Cannot both register and cancel a request.</strong></br>")
                    cleansed_form.pop(reqid)

    scrubbed = {}
    for reqid in cleansed_form:
        kv = cleansed_form[reqid]
        for k in kv:
            scrubbed[k] = kv[k]

    return scrubbed

def sanitize(web_form):
    '''Take a cgi.FieldStorage object and scrub it down to sane values.
    returns a dict with the cgi vars as keys and their html.escape()ed
    values as the values.'''
    clean_vars = {}
    for var in web_form:
        if name_ok(var):
            reqid = (var.split('_'))[-1]
            if val_ok(web_form[var].value):
                if reqid not in clean_vars:
                    clean_vars[reqid] = {}
                clean_vars[reqid][var] = html.escape(web_form[var].value)
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
    _print_err("Invalid name: {}".format(name))
    return False

def val_ok(string):
    '''Check that this is a valid value from the form.'''

    # If any character besides those listed in the character class below
    # are in the string, then we call shenanigans.  Otherwise, we'll say
    # it's legal.
    if not re.search(r'[^-a-zA-Z0-9_.@#,+ \']', string):
        return True
    _print_err("Bad value: {}".format(string))
    return False
