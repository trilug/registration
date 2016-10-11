import member
import pytest

from copy import deepcopy

#
# General Member class tests.
#
MEMBER = {'minimal':{
            'data':{
                'first':'myfn', 'last':'myln', 'addr1':'myad1', 'city':'mycty',
                'state':'st', 'zipcode':'12345', 'email':'tester@example.com'
                },
            'keys-same':True,
            'vals-same':True,
            'len-same':True}}

MEMBER['min-plus-username']                     = deepcopy(MEMBER['minimal'])
MEMBER['min-plus-username']['data']['username'] = 'myusername'

MEMBER['min-plus-addr2']                        = deepcopy(MEMBER['minimal'])
MEMBER['min-plus-addr2']['data']['addr2']       = 'myad2'

MEMBER['full']                                  = deepcopy(MEMBER['min-plus-username'])
MEMBER['full']['data']['addr2']                 = 'myad2'

MEMBER['bogus']                                 = deepcopy(MEMBER['minimal'])
MEMBER['bogus']['data']['nosuchfield']          = 'bogosity'
MEMBER['bogus']['keys-same']                    = False
MEMBER['bogus']['vals-same']                    = False
MEMBER['bogus']['len-same']                     = False

@pytest.fixture(scope='module', params=list(MEMBER.values()), ids=list(MEMBER.keys()))
def testmember(request):
    return {
            'source':request.param['data'],
            'generated':member.Member(request.param['data']),
            'vals-same':request.param['vals-same'],
            'keys-same':request.param['keys-same'],
            'len-same':request.param['len-same'],
           }

def test_values(testmember):
    assert ((set(testmember['source'].values()) == set(testmember['generated'].values()))
                == testmember['vals-same'])

def test_keys(testmember):
    assert ((set(testmember['source'].keys()) == set(testmember['generated'].keys()))
                == testmember['keys-same'])

def test_name(testmember):
    assert (testmember['generated'].name()
                == testmember['source']['first'] + ' ' + testmember['source']['last'])

def test_wants_shell(testmember):
    assert testmember['generated'].wants_shell() == ('username' in testmember['source'])

def test_shell_values(testmember):
    if testmember['generated'].wants_shell():
        assert ((testmember['generated'].shell_values()
                    == list(testmember['source'][k] for k in ('username', 'first', 'last', 'email'))))

def test_len(testmember):
    assert (len(testmember['source']) == len(testmember['generated'])) == testmember['len-same']

def test_getitem(testmember):
    for k in member.Member.field_names():
        if k in testmember['generated']:
            assert testmember['source'].get(k, None) == testmember['generated'][k]


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


#
# Test the username validator
#
USERNAMES = {
        'all_lowercase':           { 'value':'foobar',              'expected':True },
        'with_uppercase':          { 'value':'Foobar',              'expected':True },
        'with_digit':              { 'value':'foobar1',             'expected':True },
        'all_uppercase':           { 'value':'FOOBAR',              'expected':True },
        'with_dash':               { 'value':'foo-bar',             'expected':True },
        'with_dot':                { 'value':'foo.bar',             'expected':True },
        'with_underscore':         { 'value':'foo_bar',             'expected':True },
        'dot_and_dash':            { 'value':'foo.bar-blarch',      'expected':True },
        'dot_and_underscore':      { 'value':'foo.bar_blarch',      'expected':True },
        'dash_and_underscore':     { 'value':'foo-bar_blarch',      'expected':True },
        'dot_dash_and_underscore': { 'value':'foo.bar-blarch_quux', 'expected':True },
        'umlaut':                  { 'value':'fÖo',                 'expected':True },
        'accented_char':           { 'value':'renée',               'expected':True },
        'empty':                   { 'value':'',                    'expected':False },
        'leading_space':           { 'value':' foobar',             'expected':False },
        'embedded_space':          { 'value':'foo bar',             'expected':False },
        'trailing_space':          { 'value':'foobar ',             'expected':False },
        'leading_dot':             { 'value':'.foobar',             'expected':False },
        'leading_dash':            { 'value':'-foobar',             'expected':False },
        'leading_underscore':      { 'value':'_foobar',             'expected':False },
        'leading_tab':             { 'value':'	foobar',            'expected':False },
        'embedded_tab':            { 'value':'foo	bar',           'expected':False },
        'trailing_tab':            { 'value':'foobar	',          'expected':False },
        }

@pytest.fixture(scope='module', params=list(USERNAMES.values()), ids=list(USERNAMES.keys()))
def testusername(request):
    return request.param

def test_is_valid_username(testusername):
    assert member._is_valid_username(testusername['value']) == testusername['expected']


#
# Test the state validator
#
STATE = {
        'all_lowercase':  { 'value':'nc',   'expected':True },
        'with_uppercase': { 'value':'Nc',   'expected':True },
        'all_uppercase':  { 'value':'NC',   'expected':True },
        'empty':          { 'value':'',     'expected':False },
        'leading_space':  { 'value':' NC',  'expected':False },
        'embedded_space': { 'value':'N C',  'expected':False },
        'trailing_space': { 'value':'NC ',  'expected':False },
        'leading_dot':    { 'value':'.NC',  'expected':False },
        'embedded_dots':  { 'value':'N.C.', 'expected':False },
        }

@pytest.fixture(scope='module', params=list(STATE.values()), ids=list(STATE.keys()))
def teststate(request):
    return request.param

def test_is_valid_state(teststate):
    assert member._is_valid_state(teststate['value']) == teststate['expected']


#
# Test the address validator
#
ADDRESS = {
        'plain_0':        { 'value':'123 Main Street',         'expected':True },
        'plain_1':        { 'value':'#1 Main Street',          'expected':True },
        'apartment_0':    { 'value':'123 Main Street, Apt. 4', 'expected':True },
        'apartment_1':    { 'value':'123 Main Street, #4',     'expected':True },
        'po_box':         { 'value':'P.O. Box 1234',           'expected':True },
        'apostrophe':     { 'value':"123 O'Leary Street",      'expected':True },
        'empty':          { 'value':'',                        'expected':False },
        'leading_space':  { 'value':' 123 Main Street',        'expected':False },
        'trailing_space': { 'value':'123 Main Street ',        'expected':False },
        'bad_char_0':     { 'value':'123 @Main Street',        'expected':False },
        'bad_char_1':     { 'value':'123 %Main Street',        'expected':False },
        }

@pytest.fixture(scope='module', params=list(ADDRESS.values()), ids=list(ADDRESS.keys()))
def testaddress(request):
    return request.param

def test_is_valid_address(testaddress):
    assert member._is_valid_address(testaddress['value']) == testaddress['expected']


###
### TBD...
###
#    def optional_field_names(cls):
#    def __setitem__(self, key, val):
