% rebase('nap-frame.tpl',title='Submit game file')
<h1>Submit a new game file</h1>
<h3>Instructions</h3>
<ol>
<li>In the form just below, type the name of your club in the top field, and the
word "bridge" in the next field.</li>
<li>Click the "Browse" button. A file explorer window will open.</li>
<li>In the explorer window, navigate to <b>C:\ACBLSCOR\GAMEFILE</b>. This is
where ACBLscore stores game files by date.</li>
<li>Find the date and session of your NAP qualifier game. (Unfortunately if
"file extensions" are hidden, it's a little difficult to distinguish a morning
game from an afternoon game from an evening game. But if you pick the wrong one,
no harm. You can repeat with the others.)</li>
<li>Click "Submit file."</li>
</ol>
<p>Your game file will be validated and presented for your confirmation. If you
confirm, the results will immediately be added to the site.</p>
<p><i>You may also submit an ACBLscore "NAP report" which is a CSV file, in place
of the game files. Your results will appear as August 31 in the (Other) session.</i>
To submit a CSV file NAP report, follow the same steps above, but in step 2. navigate to where
the file was saved when you generated the report, and select that file.</p>
<form method="post" enctype="multipart/form-data" action="/submit_gamefile_confirm">
<p><label>Your club name:<br/><input name="clubname" size="50"/></label></p>
<p><label>Not a robot? Type the name of our game:<br/>
<input name="testfield" size="10"/></label></p>
<p><label>Click browse to select a game file (or CSV "NAP Report") to submit:<br/><input name="gamefile1" type="file"/></label></p>
<p><button class="button medium-btn">Submit file</button></p>
</form>
