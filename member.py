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
        a Member instance, or inserting into a database (the addr2 field appears at
        the end of the list, since it's optional).  The 'print' order places addr2
        directly after addr1 so that it can be used in a print format, for instance.'''
        fields = cls._fields
        if order == 'print':
            return sorted(fields.keys(), key=lambda k: fields[k][1])
        else:
            return sorted(fields.keys(), key=lambda k: fields[k][0])

    def __init__(self, first, last, addr1, city, state,
                 zipcode, email, username, addr2=None):
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

    def string_values(self, order='init'):
        '''Return the values in the Member.  This is intended for usage in
        printing.  So if addr2 isn't defined for this Member, an empty
        string is returned in its place.  In other words, this will always
        return a number of items equal to the maximum number possible for
        a Member.'''
        all_values = []
        for field in Member.ordered_field_names(order):
            if field == 'addr2' and not self._field[field]:
                all_values.append('')
            else:
                all_values.append(self._field[field])

        return all_values


    def values(self, order='init'):
        '''Return the values in the Member.  This is intended for usage in
        database insertions and such.  So if addr2 isn't defined for this
        Member, it simply isn't returned (the db should have a default set
        for the column).'''
        all_values = []
        for field in Member.ordered_field_names(order):
            if field != 'addr2' or self._field[field] != None:
                all_values.append(self._field[field])

        return all_values


    def field_names(self, order='init'):
        '''Return the names of the fields in this Member.  Intended for use
        in database insertions.  If addr2 isn't present, it is not listed
        among the fields for the Member.'''
        all_field_names = []
        for field in Member.ordered_field_names(order):
            if field != 'addr2' or self._field[field] != None:
                all_field_names.append(field)

        return all_field_names


    def field_count(self):
        '''Return the count of fields for this Member.  The only thing that
        will change this from being the same number as "all the fields" is if
        addr2 isn't set.'''
        if self._field['addr2']:
            return len(self._fields)
        else:
            return len(self._fields) - 1


    def shell_names(self):
        '''Return the fields necessary to create a shell account.'''
        return ('username', 'first', 'last', 'email')


    def shell_values(self):
        '''Return the fields necessary to create a shell account.'''
        return list(self._field[f] for f in self.shell_names())


class Requester(Member):
    '''A Member after they have been assigned a request id, generally
    one who's been fetched from the database.'''

    @classmethod
    def active_request_field_names(order='init'):
        '''Same as Member.ordered_field_names, but with the addition of the
        request id at the beginning of the field list.'''
        return ["reqid"] + Member.ordered_field_names(order)

    def __init__(self, reqid, first, last, addr1, city, state,
                 zipcode, email, username, addr2=None):
        '''Just instantiate a Member and add the request id.'''
        super(Requester, self).__init__(first, last, addr1, city, state,
                                        zipcode, email, username, addr2)
        self.reqid = reqid

    def get_reqid(self):
        '''Simple getter to return the request id of the Requester.'''
        return self.reqid
