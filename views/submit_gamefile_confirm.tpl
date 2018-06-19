% rebase('nap-frame.tpl',title='Confirm game file')
<h1>Game File Information</h1>
<p>Game File name: {{gamefile_name}}</p>
% if not is_error:
<h2>Confirm submitting Game File?</h2>
<p>
<form method="post" action="/confirm_gamefile">
<input name="upload_dir" type="hidden" value="{{upload_dir}}"/>
<input name="club_num" type="hidden" value="{{club_num}}"/>
<input name="gamefile_name" type="hidden" value="{{gamefile_name}}"/>
<input name="confirm" type="radio" value="yes" checked/>Yes, submit this game file<br/>
<input name="confirm" type="radio" value="no"/>No, discard this upload<br/>
<input type="submit" value="Submit"/>
</form>
<p>Club information found:<br/>
<pre>
{{club_info}}

{{player_summary}}
</pre>
</p>
% else:
<p>Sorry, there was an error processing this file.</p>
<p>Error messages:<br/>
<pre>
{{error_msg}}
</pre>
<p><a href="/submit_gamefile">Submit another</a></p>
% end
% end
