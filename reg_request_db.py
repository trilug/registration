import sqlite3

import member

_tablename = 'requests'

class RegDb():

    def __init__(self, dbfile):
        try:
            self._db = sqlite3.connect(dbfile)

        except sqlite3.OperationalError as oe:
            raise ConnectionError("Cannot connect to db at {}".format(dbfile)) from oe

        else:
            self._cursor = self._db.cursor()


        '''Try to create the db if it doesn't already exist.'''
        try:
            self._cursor.execute('''CREATE TABLE {} (
                                regid INTEGER PRIMARY KEY,
                                first TEXT,
                                last TEXT,
                                email TEXT unique,
                                addr1 TEXT,
                                addr2 TEXT,
                                city TEXT,
                                state TEXT,
                                zipcode INTEGER,
                                username TEXT unique)'''.format(_tablename))

        except sqlite3.OperationalError:
            pass

        else:
            self._db.commit()



    def insert(self, new_member):

        # Allowing addr2 to go through with the table default of NULL if
        # it wasn't set at instantiation.
        try:
            self._cursor.execute('''INSERT INTO {table}
                        ({fields}) VALUES ({places})'''.format(
                                table  = _tablename,
                                fields = ', '.join(new_member.field_names()),
                                places = ', '.join(list('?' * new_member.field_count()))
                            ),
                        new_member.values()
                    )

        except sqlite3.IntegrityError as ie:
            new_exception = "Unable to insert: "
            if 'username' in str(ie):
                new_exception += "username {} was previously requested.".format(new_member.username)
            elif 'email' in str(ie):
                new_exception += "email address {} is associated with a previous request.".format(new_member.username)

            raise RuntimeError(new_exception)

        else:
            self._db.commit()

    def delete(self, regid):
        try:
            self._cursor.execute(
                    '''DELETE FROM {table} WHERE regid = ?'''.format(table = _tablename),
                    regid
                )

        except:
            raise RuntimeError("Unable to delete request.")

    def candidates(self):
        # NOTE: this is the order problem.  *field_names() always includes addr2
        # embedded in the middle.  works well for process_form where we need it 
        # there to print correctly, but screws us up here when it needs to be at
        # the end as an optional arg.
        # So, we select in (..., addr1, addr2, ...) order, and create Requesters
        # off of that query.  But a Requester expects addr2 at the *end* of its
        # ctor arg list, not in the middle.  So the new Requester has a 'city' of
        # addr2, a 'state' of city, etc.  Which screws everything up downstream.
        # TODO: Fix dis shit.
        self._cursor.execute('''SELECT {fields} FROM {table}'''.format(fields = ', '.join(member.requested_field_names()), table = _tablename))

        for user in self._cursor:
            new_member = member.Requester(*user[:])
            yield new_member

