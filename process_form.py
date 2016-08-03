header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
<head>
    <title>TriLUG Membership Requests</title>
</head>

<body>
'''

footer = '</body>\n</html>'

start_form = '''<form method="POST" action="/cgi-bin/process_registrations">
<table border=1 cellpadding=2 cellspacing=1 width=80%>
'''

end_form   = '''</table>
<input type="submit" value="Submit">
<input type="reset" value="Clear">
</form>
'''

candidate_template = '''<tr>
<td><nobr><input type="checkbox" name="action{reqid}" value="reg"> Register</nobr></br>
    <input type="checkbox" name="action{reqid}" value="mod"> Modify</br>
    <input type="checkbox" name="action{reqid}" value="del"> Delete</br>
    </td>
<td><nobr><input type="text" name="first{reqid}" value="{}" size=10>
    <input type="text" name="last{reqid}" value="{}" size=10></nobr></br>
    <input type="text" name="addr1{reqid}" value="{}" size=20></br>
    <input type="text" name="addr2{reqid}" value="{}" size=20></br>
    <nobr><input type="text" name="city{reqid}" value="{}" size=20>,
    <input type="text" name="state{reqid}" value="{}" size=3>
    <input type="text" name="zipcode{reqid}" value="{}" size=6></nobr></td>
<td><strong>Email:</strong> <input type="text" name="email{reqid}" value="{}" size=20></td>
<td><strong>Requested Username:</strong>
    <input type="text" name="username{reqid}" value="{}" size=15></td>
</tr>
'''
