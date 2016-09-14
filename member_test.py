import member
import pytest

from copy import deepcopy

CASE = {'minimal':{
            'data':{
                'first':'myfn', 'last':'myln', 'addr1':'myad1', 'city':'mycty',
                'state':'st', 'zipcode':'12345', 'email':'tester@example.com'
                },
            'expected':True}}

CASE['min-plus-username'] = deepcopy(CASE['minimal'])
CASE['min-plus-username']['data']['username'] = 'myusername'

CASE['min-plus-addr2'] = deepcopy(CASE['minimal'])
CASE['min-plus-addr2']['data']['addr2'] = 'myad2'

CASE['full'] = deepcopy(CASE['min-plus-username'])
CASE['full']['data']['addr2'] = 'myad2'

CASE['bogus'] = deepcopy(CASE['minimal'])
CASE['bogus']['data']['nosuchfield'] = 'bogosity'
CASE['bogus']['expected'] = False

@pytest.fixture(scope='module', params=list(CASE.values()), ids=list(CASE.keys()))
def case(request):
    return {
            'source':request.param['data'],
            'generated':member.Member(request.param['data']),
            'expected':request.param['expected'],
           }

def test_values(case):
    assert (set(case['source'].values()) == set(case['generated'].values())) == case['expected']

def test_keys(case):
    assert (set(case['source'].keys()) == set(case['generated'].keys())) == case['expected']

def test_name(case):
    assert case['generated'].name() == case['source']['first'] + ' ' + case['source']['last']

def test_wants_shell(case):
    assert case['generated'].wants_shell() == ('username' in case['source'])

def test_shell_values(case):
    if case['generated'].wants_shell():
        assert (case['generated'].shell_values() == list(case['source'][k] for k in ('username', 'first', 'last', 'email'))) == case['expected']

def test_len(case):
    assert (len(case['source']) == len(case['generated'])) == case['expected']

###
### TBD...
###
#    def field_names(cls):
#    def optional_field_names(cls):
#    def __getitem__(self, key):
#    def __setitem__(self, key, val):
#    def __init__(self, init_vals={}):
