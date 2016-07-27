header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
<head>
    <title>TriLUG Membership Requests</title>
</head>

<body>
'''

footer = '</body>\n</html>'

def print_form():
    print('''{start}

<form method="POST" action="/cgi-bin/register">
First Name: <input type="text" name="first">  
Last Name: <input type="text" name="last"></br>
Street Address 1: <input type="text" name="addr1"></br>
Street Address 2 [optional]: <input type="text" name="addr2"></br>
City: <input type="text" name="city"> 
State: <input type="text" name="state" size=2> 
Zip: <input type="text" name ="zipcode" size=5></br>
Email: <input type="text" name="email"></br>
Preferred User ID: <input type="text" name="username"></br>
&nbsp;</br>
<input type="submit" value="Submit"> <input type="reset" value="Clear">
</form>

{end}
    '''.format(start=header, end=footer))

