import member
import pytest

USERS = [['first', 'last', 'addr1', 'city', 'state', 'zipcode', 'email']]
USERS.append(USERS[0] + ['username'])
USERS.append(USERS[0] + ['addr2'])
USERS.append(USERS[1] + ['addr2'])

@pytest.fixture(params=USERS, ids=['minimal', 'min-plus-username', 'min-plus-addr2', 'full'])
def new_member(request):
    return [request.param, member.Member(*request.param)]

def test_values(new_member):
    assert set(new_member[0]) == set(new_member[1].values())

###
### TBD...
###
#    def ordered_field_names(cls, order='init'):
#    def optional_field_names(cls):
#    def name(self):
#    def string_values(self, order='init'):
#    def values(self, order='init'):
#    def field_names(self, order='init'):
#    def field_count(self):
#    def wants_shell(self):
#    def shell_names(self):
#    def shell_values(self):
#    def active_request_field_names(order='init'):
#    def get_reqid(self):
