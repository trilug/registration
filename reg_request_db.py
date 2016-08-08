import sqlite3

from member import Requester

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
                                reqid INTEGER PRIMARY KEY,
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
                new_exception += "username {} was previously requested.".format(
                    new_member.username)
            elif 'email' in str(ie):
                new_exception += "email address {} is associated with a previous request.".format(
                    new_member.username)

            raise RuntimeError(new_exception)

        else:
            self._db.commit()


    def modify(self, reqid, field, value):
        try:
            self._cursor.execute(
                '''UPDATE {table} SET {field} = "{val}" WHERE reqid = ?'''.format(
                    table = _tablename,
                    field = field,
                    val   = value),
                reqid)

        except sqlite3.Error as e:
            raise RuntimeError("Unable to modify request: " + str(e))

        else:
            self._db.commit()


    def delete(self, reqid):
        try:
            self._cursor.execute(
                    '''DELETE FROM {table} WHERE reqid = ?'''.format(
                        table = _tablename),
                    reqid)

        except sqlite3.Error as e:
            raise RuntimeError("Unable to cancel request: " + str(e))

        else:
            self._db.commit()


    def candidates(self):
        try:
            self._cursor.execute('''SELECT {fields} FROM {table}'''.format(
                fields = ', '.join(Requester.active_request_field_names()),
                table = _tablename))

        except sqlite3.Error as e:
            raise RuntimeError("Unable to fetch requests: " + str(e))

        else:
            for user in self._cursor:
                new_member = Requester(*user[:])
                yield new_member

    def candidate(self, reqid):
        try:
            self._cursor.execute(
                    '''SELECT {fields} FROM {table} WHERE reqid = ?'''.format(
                        fields = ', '.join(Requester.active_request_field_names()),
                        table = _tablename),
                    reqid)
        except sqlite3.Error as e:
            raise RuntimeError("Unable to fetch request id {}: {}".format(
                reqid, str(e)))
        else:
            return Requester(*self._cursor.fetchone())
