header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
<head>
    <title>Join TriLUG!</title>
</head>

<body>
'''

footer = '''
<div align="center">Reload the <a href="/cgi-bin/{}">form</a></div>

</body>
</html>
'''

full_form = '''

<form method="POST" action="/cgi-bin/request_membership">
<table cellspacing="1" cellpadding="1" border="0">
<tr>
<td align="right">First Name:</td><td align="left"><input type="text" name="first"></td>
<td align="right">Last Name:</td><td align="left"><input type="text" name="last"></td>
</tr>
<tr>
<td align="right">Street Address 1:</td>
<td align="left" colspan=3><input type="text" name="addr1"></td>
</tr>
<tr>
<td align="right">Street Address 2 [optional]:</td>
<td align="left" colspan=3><input type="text" name="addr2"></td>
</tr>
<tr>
<td align="right" colspan=2>City: <input type="text" name="city"></td>
<td align="left">&nbsp;&nbsp;State: <input type="text" name="state" size=2></td>
<td align="left">&nbsp;&nbsp;Zip: <input type="text" name ="zipcode" size=5></td>
</tr>
<tr>
<td align="right">Email:</td>
<td align="left" colspan=3><input type="text" name="email"></td>
</tr>
<tr>
<td align="right">Preferred User ID:</td>
<td align="left" colspan=3><input type="text" name="username"></td>
</tr>
<tr>
<td align="center" colspan=2><input type="submit" value="Submit"></td>
<td align="center" colspan=2><input type="reset" value="Clear"></td>
</tr>
</table>
</form>

'''

