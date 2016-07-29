import sqlite3

from member import Member

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
                    '''DELETE FROM {} WHERE regid = ?'''.format(_tablename),
                    regid
                )

        except:
            raise RuntimeError("Unable to delete request.")

    def print_queue(self):
        self._cursor.execute('''SELECT
                    regid, first, last, email,
                    addr1, addr2, city, state, zipcode, username
                    FROM {}'''.format(_tablename))

        for user in self._cursor:
            print('''<p>Request Id: {}</br>
Name: {} {}</br>
Current email: {}</br>
Street Address: {}</br>'''.format(*user[:5]))
            if user[5]:
                print('                {}</br>'.format(user[5]))
            print('''City, State, Zip: {}, {} {}</br>
Preferred User ID: {}</p>
'''.format(*user[:])
            )
