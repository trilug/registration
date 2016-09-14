# TODO: Move some of the value validation and/or cleansing in here from reg_scrub

class Member():
    '''The basic class that holds a prospective member and all of his or her
    registration info.  It's not much more than a dict with some validation
    and constraints around the keys and values.'''

    _mandatory_fields = ('first', 'last', 'addr1', 'city', 'state', 'zipcode', 'email')
    _optional_fields  = ('addr2', 'username')
    _all_fields       = _mandatory_fields + _optional_fields

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
                self._field[field] = init_vals[field]

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
            self._field[key] = val

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

    def __init__(self, init_vals={}):
        '''Just instantiate a Member and add the request id.'''
        super(Requester, self).__init__({k:init_vals[k] for k in init_vals.keys() if k != 'reqid'})
        if 'reqid' in init_vals:
            self._field['reqid'] = init_vals['reqid']
