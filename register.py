import os
import urllib.parse
import urllib.request

from member import Requester


_member_to_add = {
    'first':   'first_name',
    'last':    'last_name',
    'addr1':   'address_1',
    'addr2':   'address_2',
    'city':    'city',
    'state':   'state',
    'zipcode': 'zip_code',
    'email':   'email'
    }


_datadir = '/var/spool/registration'
_queue   = '{}/new_shell_accts'.format(_datadir)
_dbfile  = '{}/account_queue.db'.format(_datadir)
database = _dbfile


def add_to_member_db(new_member):
    '''This currently backposts to the existing member tool on the
    steering site.  It will eventually directly interface with the
    database, but this is the quickest way to get us up for now.'''
    _url = 'https://steering.trilug.org/member_tool/?cmd=add'

    _varlist = list(
            (_member_to_add[v], new_member[v])
            for v in new_member.keys() if v in _member_to_add)
    _varlist.append(('submit', 'Submit'))
    _request_vars = urllib.parse.urlencode(_varlist).encode('utf-8')

    _headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }

    try:
        auth_header = os.environ['HTTP_AUTHORIZATION']
    except KeyError:
        raise RuntimeError('Unauthorized')
    else:
        _headers['Authorization'] = auth_header
        req = urllib.request.Request(_url, _request_vars, _headers)
        try:
            results = urllib.request.urlopen(req)
        except:
            raise RuntimeError("Call to add script failed.")


def queue_for_shell(new_member):
    '''Add info to the list of shell accounts to add.'''
    with open(_queue, 'a') as queue:
        queue.write('\t'.join(new_member.shell_values())+'\n')

