<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Submit Gamefile</title>
</head>
<body>
<h1>Submit a new game file</h1>
<form method="post" enctype="multipart/form-data" action="/submit_gamefile_confirm">
<p><label>Your club name:<br/><input name="clubname" size="50"/></label></p>
<p><label>Not a robot? Type the name of our game. (Hint: five letters, starts with 'b' and ends with 'e'):<br/>
<input name="testfield" size="10"/></label></p>
<p><label>Click browse to select a gamefile to submit:<br/><input name="gamefile1" type="file"/></label></p>
<p><button>Submit file</button></p>
</form>
</body>
