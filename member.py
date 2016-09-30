import re

def _is_numeric(val):
    return len(val) > 0 and re.search(r'\D', str(val)) == None

# This is a *really* loose definition of a "valid" email.  Only
# checking for basic structure, and not a lot else.
# Basically, a word character, followed by zero or more other
# word characters, dashes, dots, and plusses, followed by the
# '@' symbol, followed by a word character, followed by one or
# more groups of word characters ending with a dot, ending with
# a group of word characters and an optional dot.
def _is_valid_email(val):
    return re.match(r'\w[-\w.+]*@\w(?:[-\w]+\.)+\w+\.?\Z', val) != None

def _is_valid_name(val):
    return re.search(r"[^-\w '.]", val) == None

def _is_valid_address(val):
    return re.search(r"[^-\w '#.]", val) == None

def _is_valid_zipcode(val):
    return re.match(r'\d{5}(?:-\d{4})?\Z', val) != None

def _is_valid_username(val):
    return ((re.search(r"[^-\w.]",  val) == None) and
            (re.search(r"[a-zA-Z]", val) != None))

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
            'reqid':    _is_numeric,
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
        '''Nothing to do other than populate the data members.'''
        self._field = {}
        for field in self.__class__.field_names():
            if field in init_vals:
                self[field] = init_vals[field]

    def __contains__(self, key):
        '''Indicate whether a field is set for the Member.'''
        if key in self._field:
            return True
        return False

    def __getitem__(self, key):
        '''Retrieve the values of one of the fields.'''
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
        if ('username' in self._field) and self['username']:
            return True
        return False

    def shell_values(self):
        '''Return the fields necessary to create a shell account.'''
        return list(self[f] for f in ('username', 'first', 'last', 'email'))


class Requester(Member):
    '''A Member after they have been assigned a request id, generally
    one who's been fetched from the database.'''

    _mandatory_fields = Member._mandatory_fields + tuple(['reqid'])
    _all_fields       = _mandatory_fields + Member._optional_fields
