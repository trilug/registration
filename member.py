import re

# Thin wrapper around a Python built-in, but it allows for a uniform
# validation interface below.
def _is_integer(val):
    return isinstance(val, int)

# This is a *really* loose definition of a "valid" email.  Only checking
# for basic structure, and not a lot else.  Basically, a word character,
# followed by zero or more other word characters, dashes, dots, and plusses,
# followed by the '@' symbol, followed by a word character, followed by one
# or more groups of word characters ending with a dot, ending with a group
# of word characters and an optional dot.
def _is_valid_email(val):
    return re.match(r'\w[-\w.+]*@\w(?:[-\w]+\.)+\w+\.?\Z', val) != None

# A valid name: A) contains only alphanumeric characters, dots, dashes,
# apostrophes, commas, and spaces; and B) contains at least one letter.
# The first regex asserts that the value does not contain any character
# which is NOT one of the aforementioned types.  The second asserts that
# it starts with a character that is not a dash space, apostrophe, dot,
# or number; ie - a letter.  We can't just use "^[A-Za-z]", because that
# doesn't include such things as accented characters.
def _is_valid_name(val):
    return ((re.search(r"[^-\w '.,]", val) == None) and
            (re.search(r"\A[^-0-9 '.]", val) != None))

# This is a really loose definition of "valid address" - we're pretty
# much just whitelisting characters we consider okay to have in an
# address and making sure it's not empty.
def _is_valid_address(val):
    return ((len(val) > 0) and
            (re.search(r"[^-\w '#.,]", val) == None) and
            (re.search(r"\A\S", val) != None) and
            (re.search(r"\S\Z", val) != None))

# Strictly either 5 digits, or 5 digits, a dash, and 4 digits.
def _is_valid_zipcode(val):
    return re.match(r'\d{5}(?:-\d{4})?\Z', val) != None

# A username can't contain anything but dots, dashes, and word characters,
# and must begin with a letter.
def _is_valid_username(val):
    return ((re.search(r"[^-\w.]",  val) == None) and
            (re.search(r"^[a-zA-Z]", val) != None))

# Yeah, ok, so "ZZ" isn't actually a "valid" state, for example.  We'll
# deal with that when it becomes a real issue.  :P
def _is_valid_state(val):
    return re.search(r'\A[a-zA-Z][a-zA-Z]\Z', val) != None

class Member():
    '''The basic class that holds a prospective member and all of his or her
    registration info.  It's not much more than a dict with some validation
    and constraints around the keys and values.'''

    _mandatory_fields = ('first', 'last', 'addr1', 'city', 'state',
                         'zipcode', 'email')
    _optional_fields  = ('addr2', 'username')
    _all_fields       = _mandatory_fields + _optional_fields

    _valid_field = {
            'first':    _is_valid_name,
            'last':     _is_valid_name,
            'addr1':    _is_valid_address,
            'addr2':    lambda f: f == None or _is_valid_address(f),
            'city':     _is_valid_name,
            'state':    _is_valid_state,
            'zipcode':  _is_valid_zipcode,
            'email':    _is_valid_email,
            'username': lambda f: f == None or _is_valid_username(f),
        }

    @classmethod
    def field_names(cls):
        '''What it says on the tin.  Return the names of the fields in the
        Member (or, eventually, Requester) class.'''
        return cls._all_fields

    @classmethod
    def optional_field_names(cls):
        '''Just return a list of the optional fields.'''
        return cls._optional_fields

    def __init__(self, init_vals={}):
        '''Nothing to do other than populate the data members.  We ignore
        any spurious fields that are provided in the input by using the
        Member field names as the source of key names to set and only
        setting those which are found in init_vals.  Note that validation
        of the values is delegated to the __setitem__ method.'''
        self._field = {}
        for field in self.__class__.field_names():
            if field in init_vals:
                self[field] = init_vals[field]

    def __contains__(self, key):
        '''Indicate whether a field is set for the Member.'''
        return key in self._field

    def __getitem__(self, key):
        '''Retrieve the values of one of the fields.  We allow the regular
        Python KeyError to be thrown on a bad field name.  No need to set
        anything special up for that.'''
        return self._field[key]

    def __setitem__(self, key, val):
        '''Set the value of one of the fields.'''
        if key in self.__class__.field_names():
            if self.__class__._valid_field[key](val):
                self._field[key] = str(val).strip()

    def __len__(self):
        '''In many ways emulating a dict, so len(m) should work.'''
        return sum(1 for f in self._field if self._field[f])

    def keys(self):
        '''Dict emulation.  Provide the keys in the _field dict.'''
        return self._field.keys()

    def values(self):
        '''Dict emulation.  Provide the values in the _field dict.'''
        return self._field.values()

    def name(self):
        '''Return the name of the Member as "first last".'''
        return "{} {}".format(self['first'], self['last'])

    def wants_shell(self):
        '''Returns a boolean indicating whether or not the new member has
        requested shell/email access.'''
        return bool(('username' in self._field) and self['username'])

    def shell_values(self):
        '''Return the fields necessary to create a shell account.'''
        return list(self[f] for f in ('username', 'first', 'last', 'email'))


class Requester(Member):
    '''A Member after they have been assigned a request id.  Probably
    one who's been fetched from the database.'''

    _mandatory_fields     = Member._mandatory_fields + tuple(['reqid'])
    _all_fields           = Member._all_fields       + tuple(['reqid'])
    _valid_field          = Member._valid_field
    _valid_field['reqid'] = _is_integer
