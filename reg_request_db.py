import sqlite3
import sys

class RegDb():

    def __init__(self, dbfile):
        try:
            self._db = sqlite3.connect(dbfile)
        except sqlite3.OperationalError as oe:
            # TODO: Make this re-raise the exception up the stack rather
            #       than a print-and-die.
            print("Cannot connect to db at {}: {}".format(oe))
            sys.exit(1)
        else:
            self._cursor = self._db.cursor()

        '''Try to create the db if it doesn't already exist.'''
        try:
            self._cursor.execute('''CREATE TABLE requests (
                                regid INTEGER PRIMARY KEY,
                                first TEXT,
                                last TEXT,
                                email TEXT unique,
                                addr1 TEXT,
                                addr2 TEXT,
                                city TEXT,
                                state TEXT,
                                zipcode INTEGER,
                                username TEXT unique)''')
        except sqlite3.OperationalError as oe:
            pass
        else:
            self._db.commit()



    # first, last, email, addy1, addy2, city, state, zipcode, username
    def insert(self, first, last, email, addr1,
            city, state, zipcode, username, addr2=None):
        try:
            if addr2:
                self._cursor.execute('''INSERT INTO requests
                    (first, last, email, addr1, addr2, city, state, zipcode, username)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (first, last, email, addr1, addr2, city, state, zipcode, username))
            else:
                self._cursor.execute('''INSERT INTO requests
                    (first, last, email, addr1, city, state, zipcode, username)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (first, last, email, addr1, city, state, zipcode, username))
        except sqlite3.IntegrityError as ie:
            # TODO: Make this re-raise up the stack rather than printing.
            print("Unable to insert: ", end='')
            if 'username' in str(ie):
                print("username {} was previously requested.</br>".format(username))
            elif 'email' in str(ie):
                print("email address {} is associated with a previous request.</br>".format(email))
            print()
        else:
            self._db.commit()

    def delete(self, regid):
        # TODO: set up try/catch with sqlite3.OperationalError
        self._cursor.execute('''DELETE FROM requests WHERE regid = ?''', regid)

    def print_queue(self):
        self._cursor.execute('''SELECT
                    regid, first, last, email,
                    addr1, addr2, city, state, zipcode, username
                    FROM requests''')
        for user in self._cursor:
            # Thought about making these simple positional parameters to format
            # and then just passing '*user[:]', but the names make this a bit
            # more self-documenting.  The internal debate rages on, though. :)
            print('''Request Id: {reqid}</br>
Name: {first} {last}</br>
Current email: {email}</br>
Street Address: {addr1}</br>
                {addr2}</br>
City, State, Zip: {city}, {state} {zipcode}</br>
Preferred User ID: {userid}</br>
&nbsp;</br>
    '''.format(
                reqid=user[0],
                first=user[1],
                last=user[2],
                email=user[3],
                addr1=user[4],
                addr2=user[5],
                city=user[6],
                state=user[7],
                zipcode=user[8],
                userid=user[9],
                )
            )
