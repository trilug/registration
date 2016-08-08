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


_datadir  = '/var/spool/registration'
_queue    = '{}/new_shell_accts'.format(_datadir)
_dbfile   = '{}/account_queue.db'.format(_datadir)
database = _dbfile


def add_to_member_db(new_member):
    _url = 'https://steering.trilug.org/member_tool/?cmd=add'
    _vals = urllib.parse.urlencode(
            list((_member_to_add[v], new_member[v])
            for v in new_member.shell_names())).encode('ascii')
    _headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }

    try:
        auth_header = os.environ['HTTP_AUTHORIZATION']
    except KeyError:
        raise RuntimeError('Unauthorized')
    else:
        _headers['Authorization'] = auth_header
        req = urllib.request.Request(_url, _vals, _headers)
        results = urllib.request.urlopen(req)


def queue_for_shell(new_member):
    with open(_queue, 'a') as queue:
        queue.write('\t'.join(*new_member.shell_values()))

