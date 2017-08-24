<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Submit Game File Result</title>
</head>
<body>
<h1>Game File Information</h1>
<p>Game File name: {{gamefile_name}}</p>
<p>Club information found:<br/>
<pre>
{{club_info}}

{{player_summary}}
</pre>
</p>
<p>Error messages:<br/>
<pre>
{{error_msg}}
</pre>
<h2>Confirm submitting Game File?</h2>
<p>
<form method="post" action="/confirm_gamefile">
<input name="club_dir" type="hidden" value="{{club_dir}}"/>
<input name="gamefile_name" type="hidden" value="{{gamefile_name}}"/>
<input name="confirm" type="radio" value="yes" checked/>Yes, submit this game file<br/>
<input name="confirm" type="radio" value="no"/>No, discard this upload<br/>
<input type="submit" value="Submit"/>
</form>
</p>
</body>
