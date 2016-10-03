import member
import pytest

from copy import deepcopy

# General Member class tests.
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


#
# Test the zipcode validator
#
ZIPS = {
        'plain':                      { 'value':'12345',       'expected':True },
        'leading_zero':               { 'value':'01234',       'expected':True },
        'extended':                   { 'value':'12345-6789',  'expected':True },
        'extended_leading_zero':      { 'value':'12345-0678',  'expected':True },
        'empty':                      { 'value':'',            'expected':False },
        'too_short':                  { 'value':'1234',        'expected':False },
        'too_long':                   { 'value':'123456',      'expected':False },
        'too_many_fields':            { 'value':'12345-67-89', 'expected':False },
        'non_numeric':                { 'value':'X2345',       'expected':False },
        'no_first_field':             { 'value':'-1234',       'expected':False },
        'plain_leading_spaces':       { 'value':' 12345',      'expected':False },
        'plain_trailing_spaces':      { 'value':'12345 ',      'expected':False },
        'plain_embedded_spaces':      { 'value':'123 45',      'expected':False },
        'extended_leading_spaces':    { 'value':' 12345-6789', 'expected':False },
        'extended_trailing_spaces':   { 'value':'12345-6789 ', 'expected':False },
        'extended_embedded_spaces_1': { 'value':'123 45-6789', 'expected':False },
        'extended_embedded_spaces_2': { 'value':'12345 -6789', 'expected':False },
        'extended_embedded_spaces_3': { 'value':'12345- 6789', 'expected':False },
        'extended_embedded_spaces_4': { 'value':'12345-67 89', 'expected':False },
        }

@pytest.fixture(scope='module', params=list(ZIPS.values()), ids=list(ZIPS.keys()))
def testzip(request):
    return request.param

def test_is_valid_zipcode(testzip):
    assert member._is_valid_zipcode(testzip['value']) == testzip['expected']


#
# Test the numeric validator
#
NUMS = {
        'plain':                   { 'value':'12345',       'expected':True },
        'leading_zero':            { 'value':'01234',       'expected':True },
        'float':                   { 'value':'12345.6789',  'expected':False },
        'with_letter':             { 'value':'X2345',       'expected':False },
        'no_number':               { 'value':'Spam',        'expected':False },
        'empty':                   { 'value':'',            'expected':False },
        'plain_leading_spaces':    { 'value':' 12345',      'expected':False },
        'plain_trailing_spaces':   { 'value':'12345 ',      'expected':False },
        'plain_embedded_spaces':   { 'value':'123 45',      'expected':False },
        'float_leading_spaces':    { 'value':' 12345.6789', 'expected':False },
        'float_trailing_spaces':   { 'value':'12345.6789 ', 'expected':False },
        'float_embedded_spaces_1': { 'value':'123 45.6789', 'expected':False },
        'float_embedded_spaces_2': { 'value':'12345 .6789', 'expected':False },
        'float_embedded_spaces_3': { 'value':'12345. 6789', 'expected':False },
        'float_embedded_spaces_4': { 'value':'12345.67 89', 'expected':False },
        }

@pytest.fixture(scope='module', params=list(NUMS.values()), ids=list(NUMS.keys()))
def testnum(request):
    return request.param

def test_is_numeric(testnum):
    assert member._is_numeric(testnum['value']) == testnum['expected']

#
# Test the email validator
#
EMAILS = {
    'plain':                    { 'value':'foo@example.com',      'expected':True },
    'trailing_dash':            { 'value':'foo-@example.com',     'expected':True },
    'trailing_dashes':          { 'value':'foo--@example.com',    'expected':True },
    'trailing_plus':            { 'value':'foo+@example.com',     'expected':True },
    'embedded_plus':            { 'value':'foo+bar@example.com',  'expected':True },
    'embedded_plusses':         { 'value':'foo++bar@example.com', 'expected':True },
    'embedded_dot':             { 'value':'foo.bar@example.com',  'expected':True },
    'embedded_dots':            { 'value':'foo..bar@example.com', 'expected':True },
    'embedded_underscore':      { 'value':'foo_bar@example.com',  'expected':True },
    'embedded_underscores':     { 'value':'foo__bar@example.com', 'expected':True },
    'at_host':                  { 'value':'foo@test.example.com', 'expected':True },
    'at_long_host':             { 'value':'foo@oh.how.i.love.to.test.example.com',
                                                                  'expected':True },
    'domain_with_dash':         { 'value':'foo@test-example.com', 'expected':True },
    'domain_with_underscore':   { 'value':'foo@test_example.com', 'expected':True },
    'empty':                    { 'value':'',                     'expected':False },
    'domain_no_tld':            { 'value':'foo@example',          'expected':False },
    'domain_no_tld_with_dot':   { 'value':'foo@example.',         'expected':False },
    'domain_only_tld':          { 'value':'foo@.com',             'expected':False },
    'name_leading_bad_char':    { 'value':'#foo@example.com',     'expected':False },
    'name_embedded_bad_char':   { 'value':'fo#o@example.com',     'expected':False },
    'name_trailing_bad_char':   { 'value':'foo#@example.com',     'expected':False },
    'domain_leading_bad_char':  { 'value':'foo@#example.com',     'expected':False },
    'domain_embedded_bad_char': { 'value':'foo@ex#ample.com',     'expected':False },
    'domain_trailing_bad_char': { 'value':'foo@example#.com',     'expected':False },
    'tld_leading_bad_char':     { 'value':'foo@example.#com',     'expected':False },
    'tld_embedded_bad_char':    { 'value':'foo@example.co#m',     'expected':False },
    'tld_trailing_bad_char':    { 'value':'foo@example.com#',     'expected':False },
    'name_leading_space':       { 'value':' foo@example.com',     'expected':False },
    'name_embedded_space':      { 'value':'fo o@example.com',     'expected':False },
    'name_trailing_space':      { 'value':'foo @example.com',     'expected':False },
    'domain_leading_space':     { 'value':'foo@ example.com',     'expected':False },
    'domain_embedded_space':    { 'value':'foo@ex ample.com',     'expected':False },
    'domain_trailing_space':    { 'value':'foo@example .com',     'expected':False },
    'tld_leading_space':        { 'value':'foo@example. com',     'expected':False },
    'tld_embedded_space':       { 'value':'foo@example.co m',     'expected':False },
    'tld_trailing_space':       { 'value':'foo@example.com ',     'expected':False },
    }

@pytest.fixture(scope='module', params=list(EMAILS.values()), ids=list(EMAILS.keys()))
def testemail(request):
    return request.param

def test_is_valid_email(testemail):
    assert member._is_valid_email(testemail['value']) == testemail['expected']


#
# Test the name validator
#
NAMES = {
        'single':               { 'value':'Linus',              'expected':True },
        'full':                 { 'value':'Linus Torvalds',     'expected':True },
        'hyphenated':           { 'value':'Betty Smith-Rubble', 'expected':True },
        'with_apostrophe':      { 'value':"Eblis O'Shaunnesy",  'expected':True },
        'with_number':          { 'value':'Mary Smith the 3rd', 'expected':True },
        'with_comma':           { 'value':'Barney Smith, Jr',   'expected':True },
        'with_comma_and_dot':   { 'value':'Barney Smith, Jr.',  'expected':True },
        'with_initials':        { 'value':'I.C. You',           'expected':True },
        'leading_umlaut':       { 'value':'Öscar the Grouch',   'expected':True },
        'accented_char':        { 'value':'Renée',              'expected':True },
        'empty':                { 'value':'',                   'expected':False },
        'plain_leading_spaces': { 'value':' Linus',             'expected':False },
        'leading_dot':          { 'value':'.Linus',             'expected':False },
        'bad_char':             { 'value':'Robot #3',           'expected':False },
        'tab_char':             { 'value':'Erin	Smith',         'expected':False },
        }

@pytest.fixture(scope='module', params=list(NAMES.values()), ids=list(NAMES.keys()))
def testname(request):
    return request.param

def test_is_valid_name(testname):
    assert member._is_valid_name(testname['value']) == testname['expected']


###
### TBD...
###
#    def field_names(cls):
#    def optional_field_names(cls):
#    def __getitem__(self, key):
#    def __setitem__(self, key, val):
#    def __init__(self, init_vals={}):
#    def __contains__(self, key):
#    def __len__(self):
#    def keys(self):
#    def values(self):
#    def name(self):
#    def wants_shell(self):
#    def shell_values(self):
# def _is_valid_address(val):
# def _is_valid_username(val):
# def _is_valid_state(val):
