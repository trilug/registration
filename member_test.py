import unittest

import member

class MemberTests(unittest.TestCase):

    def test_values_noaddr2_init_order(self):
        user1 = ('first', 'last', 'addr1', 'city', 'state', 'zipcode', 'email', 'username')
        nm = member.Member(*user1)
        self.assertEqual(list(user1),
                list(nm.values()),
                "Bad strings.\nExpected: {}\n     Got: {}\n".format(
                    ', '.join(user1),
                    ', '.join(nm.values())))

    def test_values_noaddr2_print_order(self):
        user1 = ('first', 'last', 'addr1', 'city', 'state', 'zipcode', 'email', 'username')
        nm = member.Member(*user1)
        self.assertEqual(list(user1),
                list(nm.values('print')),
                "Bad strings.\nExpected: {}\n     Got: {}\n".format(
                    ', '.join(user1),
                    ', '.join(nm.values('print'))))

if __name__ == "__main__":
    unittest.main()

#    def ordered_field_names(cls, order='init'):
#    def __init__(self, first, last, addr1, city, state,
#    def string_values(self, order='init'):
#    def values(self, order='init'):
#    def field_names(self, order='init'):
#    def field_count(self):
#    def active_request_field_names(order='init'):
#    def __init__(self, reqid, first, last, addr1, city, state,
#    def get_reqid(self):
