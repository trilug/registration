import unittest

import member

class MemberTests(unittest.TestCase):

    def test_noaddr2(self):
        user1 = ('first', 'last', 'addr1', 'city', 'state', 'zipcode', 'email', 'username')
        nm = member.Member(*user1)
        self.assertEqual(user1, nm.string_values(), "Bad strings.\nExpected: {}\n     Got: {}\n".format(', '.join(user1), ', '.join(nm.string_values())))

if __name__ == "__main__":
    unittest.main()

