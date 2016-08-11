class Member():
    '''The basic class that holds a prospective member and all of his or her
    registration info.'''

    # The elements of this dict are:
    #     'field name': [ ordinal for constructor, ordinal for printing ]
    _fields = {'first': [0, 0], 'last':     [1, 1], 'addr1':   [2, 2], 'addr2': [8, 3],
               'city':  [3, 4], 'state':    [4, 5], 'zipcode': [5, 6],
               'email': [6, 7], 'username': [7, 8]}

    @classmethod
    def ordered_field_names(cls, order='init'):
        '''What it says on the tin.  Return the names of the fields in the Member
        class, in the specified order.  The 'init' order is appropriate for creating
        a Member instance, or inserting into a database (the optional fields appear at
        the end of the list).  The 'print' order places addr2 directly after addr1 so
        that it can be used in a print format, for instance.'''
        fields = cls._fields
        if order == 'print':
            return sorted(fields.keys(), key=lambda k: fields[k][1])
        else:
            return sorted(fields.keys(), key=lambda k: fields[k][0])

    # Optional fields
    _optional_fields = ('addr2', 'username')

    @classmethod
    def optional_field_names(cls):
        '''Just return a list of the optional fields.'''
        return cls._optional_fields

    def __init__(self, first, last, addr1, city, state,
                 zipcode, email, username=None, addr2=None):
        '''Nothing to do other than populate the data members.'''
        self._field = {}
        self._field['first']    = first
        self._field['last']     = last
        self._field['addr1']    = addr1
        self._field['addr2']    = addr2
        self._field['city']     = city
        self._field['state']    = state
        self._field['zipcode']  = zipcode
        self._field['email']    = email
        self._field['username'] = username


    def __getitem__(self, key):
        '''Retrieve the values of one of the fields.'''
        return self._field[key]

    def __setitem__(self, key, val):
        '''Set the value of one of the fields.'''
        if key in self._fields:
            self._field[key] = val

    def name(self):
        '''Return the name of the Member as "first last".'''
        return "{} {}".format(self['first'], self['last'])

    def string_values(self, order='init'):
        '''Return the values in the Member.  This is intended for usage in
        printing.  So if an optional field isn't defined for this Member, an
        empty string is returned in its place.  In other words, this will
        always return a number of items equal to the maximum number possible
        for a Member.'''
        all_values = []
        for field in Member.ordered_field_names(order):
            if field in Member.optional_field_names() and not self[field]:
                all_values.append('')
            else:
                all_values.append(self[field])

        return all_values


    def values(self, order='init'):
        '''Return the values in the Member.  This is intended for usage in
        database insertions and such.  So if one of the optional fields isn't
        defined for this Member, it simply isn't returned (the db should have
        a default set for the column).'''
        all_values = []
        for field in Member.ordered_field_names(order):
            if field not in Member.optional_field_names() or self[field] != None:
                all_values.append(self[field])

        return all_values


    def field_names(self, order='init'):
        '''Return the names of the fields in this Member.  Intended for use
        in database insertions.  If one of the optional fields isn't present,
        it is not listed among the fields for the Member.'''
        all_field_names = []
        for field in Member.ordered_field_names(order):
            if field not in Member.optional_field_names() or self[field] != None:
                all_field_names.append(field)

        return all_field_names


    def field_count(self):
        '''Return the count of fields for this Member.  The only thing that
        will change this from being the same number as "all the fields" is if
        one or more of the optional fields isn't set.'''
        missing_count = sum(1 for f in Member.optional_field_names() if not self[f])
        return len(Member.ordered_field_names()) - missing_count


    def wants_shell(self):
        '''Returns a boolean indicating whether or not the new member has
        requested shell/email access.'''
        if self['username']:
            return True
        return False

    def shell_names(self):
        '''Return the fields necessary to create a shell account.'''
        return ('username', 'first', 'last', 'email')


    def shell_values(self):
        '''Return the fields necessary to create a shell account.'''
        return list(self[f] for f in self.shell_names())


class Requester(Member):
    '''A Member after they have been assigned a request id, generally
    one who's been fetched from the database.'''

    @classmethod
    def active_request_field_names(order='init'):
        '''Same as Member.ordered_field_names, but with the addition of the
        request id at the beginning of the field list.'''
        return ["reqid"] + Member.ordered_field_names(order)

    def __init__(self, reqid, first, last, addr1, city, state,
                 zipcode, email, username=None, addr2=None):
        '''Just instantiate a Member and add the request id.'''
        super(Requester, self).__init__(first, last, addr1, city, state,
                                        zipcode, email, username, addr2)
        self.reqid = reqid

    def get_reqid(self):
        '''Simple getter to return the request id of the Requester.'''
        return self.reqid
