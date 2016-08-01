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
<td>| <input type="checkbox" name="action{reqid}" value="reg"> Register
    | <input type="checkbox" name="action{reqid}" value="mod"> Modify
    | <input type="checkbox" name="action{reqid}" value="del"> Delete
    |</td>
<td><input type="text" name="first{reqid}" value="{}">
    <input type="text" name="last{reqid}" value="{}"></td>
<td><input type="text" name="addr1{reqid}" value="{}"></br>
    <input type="text" name="addr2{reqid}" value="{}"></td>
<td><input type="text" name="city{reqid}" value="{}">,
    <input type="text" name="state{reqid}" value="{}">
    <input type="text" name="zipcode{reqid}" value="{}"></td>
<td><input type="text" name="email{reqid}" value="{}"></td>
<td><input type="text" name="username{reqid}" value="{}"></td>
</tr>
'''
