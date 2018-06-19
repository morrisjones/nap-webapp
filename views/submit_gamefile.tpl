% rebase('nap-frame.tpl',title='Submit game file')
<h1>Submit a new game file</h1>
<h3>Instructions</h3>
<ol>
<li>Click the "Browse" button. A file explorer window will open.</li>
<li>In the explorer window, navigate to <b>C:\ACBLSCOR\GAMEFILE</b>. This is
where ACBLscore stores game files by date.</li>
<li>Find the date and session of your NAP qualifier game.<br/><div style="margin-left: 25px;">(Unfortunately if
"file extensions" are hidden, it's a little difficult to distinguish a morning
game from an afternoon game from an evening game from a Bridgemate file.
But if you pick the wrong one, no harm. You can repeat with the others.)</div></li>
<li>Click "Submit file."<br/><div style="margin-left: 25px;">On your first submission, you may be
asked a CAPTCHA question to prove that you're not a robot.</div></li>
</ol>

<p>Your game file will be validated and presented for your confirmation. If you
confirm, the results will immediately be added to the site.</p>

<p><i>You may also submit an ACBLscore "NAP report" which is a CSV file, in place
of the game files. Your results will appear as August 31 in the (Other) session.</i>
To submit a CSV file NAP report, follow the same steps above, but in step 2. navigate to where
the file was saved when you generated the report, and select that file.</p>

<form name="gamefile" method="post" enctype="multipart/form-data" action="/submit_gamefile_confirm">

<script src='https://www.google.com/recaptcha/api.js'></script>
<p><label>Click browse to select a game file (or CSV "NAP Report") to submit:<br/>&nbsp;<br/><input name="gamefile1" type="file"/></label></p>
<script type="text/javascript">
function submitform() {
    document.gamefile.submit();
}
</script>
<button style="font-size: 100%;" class="g-recaptcha"
    data-sitekey="6LdbS18UAAAAAMmYPKVpeWGw60Sq6QasY3iAS2bU"
    data-callback="submitform">Submit</button>
</form>
