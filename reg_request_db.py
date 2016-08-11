import sqlite3

from member import Requester

_tablename = 'requests'

class RegDb():
    '''The database where registration requests are tracked.'''

    def __init__(self, dbfile):
        '''Open the database connection.  Create the table if it doesn't
        exist already.'''
        try:
            self._db = sqlite3.connect(dbfile)

        except sqlite3.OperationalError as oe:
            raise RuntimeError("Cannot connect to db at {}".format(dbfile)) from oe

        else:
            self._cursor = self._db.cursor()


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
        '''Add a Member to the request queue.'''

        # Allowing optional fields to go through with the table default of NULL
        # if they weren't set at instantiation.
        try:
            self._cursor.execute('''INSERT INTO {table}
                        ({fields}) VALUES ({places})'''.format(
                                table  = _tablename,
                                fields = ', '.join(new_member.field_names()),
                                places = ', '.join(list('?' * new_member.field_count()))
                            ),
                        new_member.values()
                    )

        # Tailor the exception depending on why the insertion failed.
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
        '''Alter a field in a membership request.'''
        try:
            self._cursor.execute(
                '''SELECT {field} FROM {table} WHERE reqid = ?'''.format(
                    field = field,
                    table = _tablename),
                (reqid,))

        except sqlite3.Error as e:
            raise RuntimeError("Unable to access request: " + str(e))

        else:
            old_value = str((self._cursor.fetchone())[0])
            if old_value != value:
                try:
                    self._cursor.execute(
                        '''UPDATE {table} SET {field} = "{val}" WHERE reqid = ?'''.format(
                            table = _tablename,
                            field = field,
                            val   = value),
                        (reqid,))

                except sqlite3.Error as e:
                    raise RuntimeError("Unable to modify request: " + str(e))

                else:
                    self._db.commit()
                    return True
            else:
                return False


    def delete(self, reqid):
        '''Cancel a membership request by id.'''
        try:
            self._cursor.execute(
                    '''DELETE FROM {table} WHERE reqid = ?'''.format(
                        table = _tablename),
                    (reqid,))

        except sqlite3.Error as e:
            raise RuntimeError("Unable to cancel request: " + str(e))

        else:
            self._db.commit()


    def candidates(self):
        '''Fetch all pending membership requests.'''
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
        '''Return a single membership request by id.'''
        try:
            self._cursor.execute(
                    '''SELECT {fields} FROM {table} WHERE reqid = ?'''.format(
                        fields = ', '.join(Requester.active_request_field_names()),
                        table = _tablename),
                    (reqid,))
        except sqlite3.Error as e:
            raise RuntimeError("Unable to fetch request id {}: {}".format(
                reqid, str(e)))
        else:
            return Requester(*self._cursor.fetchone())
