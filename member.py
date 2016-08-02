_fields = {'first': 0, 'last': 1, 'addr1': 2, 'addr2': 3, 'city': 4,
           'state': 5, 'zipcode': 6, 'email': 7, 'username': 8}

def ordered_field_names():
    return sorted(list(_fields.keys()), key=lambda k: _fields[k])

class Member():
    def __init__(self, first, last, addr1, city, state,
                 zipcode, email, username, addr2=None):
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


    # addr2 is a special snowflake for now - an optional field.
    # I'm not pleased with having a specific setter like this,
    # but it's a half step better than the caller directly setting
    # the value.  Blech.
    def set_addr2(self, val):
        self._field['addr2'] = val


    def string_values(self):
        all_values = []
        for field in ordered_field_names():
            if field == 'addr2' and not self._field[field]:
                all_values.append('')
            else:
                all_values.append(self._field[field])

        return all_values


    def values(self):
        all_values = []
        for field in ordered_field_names():
            if field != 'addr2' or self._field[field] != None:
                all_values.append(self._field[field])

        return all_values


    def field_names(self):
        all_field_names = []
        for field in ordered_field_names():
            if field != 'addr2' or self._field[field] != None:
                all_field_names.append(field)

        return all_field_names


    # This can be cleaner if we ever move to using a dict for the fields,
    # but this will do for the moment.
    def field_count(self):
        if self._field['addr2']:
            return len(_fields)
        else:
            return len(_fields) - 1


class Requester(Member):
    def __init__(self, regid, first, last, addr1, city, state,
                 zipcode, email, username, addr2=None):
        super(Requester, self).__init__(first, last, email, addr1, city,
                                        state, zipcode, username, addr2)
        self.regid = regid

    def reqid(self):
        return self.regid

def requested_field_names():
    return ["regid"] + ordered_field_names()
