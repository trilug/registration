header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
<head>
    <title>TriLUG Membership Requests</title>
</head>

<body>
'''

footer = '''
<div align="center">
<hr width="50%">
Reload the <a href="/cgi-bin/{}">form</a>
<strong>|</strong>
Go to the <a href="/member_tool/">Member Tool</a>
<strong>|</strong>
Back to <a href="/">Steering</a>
</div>

</body>
</html>
'''

start_form = '''<form method="POST" action="/cgi-bin/process_registrations">
<div align="center">
<table border="0" width="60%"><tr><td>
<p>Here is the list of people who have requested to join TriLUG.  The bylaws state that in order to
qualify for membership, one must attend a meeting in person.  Since this process is now being done
online, you should only register those who actually show up, rather than accepting all pending
requests.</p>

<p>Once you have registered one or more prospective members below, they will be in the member
database, but <strong>will not</strong> have a shell account.  In order to complete that process,
log on to pilot, and run:
    <pre>
    bash$ /usr/local/bin/new-accounts-from-file /var/spool/registration/new_shell_accts
    bash$ sudo rm /var/spool/registration/new_shell_accts
    </pre>
Once that is done, they're all set up.</p>
</td></tr></table>
</div>

<div align="center">
<table border=1 cellpadding=2 cellspacing=1 width=80%>
'''

end_form = '''</table>
</br>
<table border="0" width="40%"><tr>
<td align="center"><input type="submit" name="act" value="Submit"></td>
<td align="center"><input type="reset" value="Reset Form"></td>
</tr></table>
</br>
</div>
</form>
'''

candidate_template = '''<tr>
<td><strong>Request {reqid}</strong></br>
    <nobr><input type="checkbox" name="reg_{reqid}" value="1"> Register</nobr></br>
    <input type="checkbox" name="mod_{reqid}" value="1"> Modify</br>
    <input type="checkbox" name="del_{reqid}" value="1"> Cancel Request</br>
    </td>
<td><nobr><input type="text" name="first_{reqid}" value="{}" size=10>
    <input type="text" name="last_{reqid}" value="{}" size=10></nobr></br>
    <input type="text" name="addr1_{reqid}" value="{}" size=20></br>
    <input type="text" name="addr2_{reqid}" value="{}" size=20></br>
    <nobr><input type="text" name="city_{reqid}" value="{}" size=20>,
    <input type="text" name="state_{reqid}" value="{}" size=3>
    <input type="text" name="zipcode_{reqid}" value="{}" size=6></nobr></td>
<td><strong>Email:</strong> <input type="text" name="email_{reqid}" value="{}" size=20></td>
<td><strong>Requested Username:</strong>
    <input type="text" name="username_{reqid}" value="{}" size=15></td>
</tr>
'''
