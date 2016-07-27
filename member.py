class Member():
    def __init__(self, first, last, email, addr1,
            city, state, zipcode, username, addr2=None):
		self.first    = first
		self.last     = last
		self.email    = email
		self.addr1    = addr1
		self.city     = city
		self.state    = state
		self.zipcode  = zipcode
		self.username = username
		self.addr2    = addr2

    def values(self):
        all_values = (self.first, self.last, self.email, self.addr1)
        if self.addr2 != None:
            all_values.append(self.addr2)
		all_values.append(self.city, self.state, self.zipcode, self.username)

        return all_values

    def field_names(self):
        all_field_names = ('first', 'last', 'email', 'addr1')
        if self.addr2 != None:
            all_field_names.append('addr2')
		all_field_names.append('city', 'state', 'zipcode', 'username')

        return all_field_names

    def field_count(self):
        if self.addr2 == None:
            return 8
        else:
            return 9

