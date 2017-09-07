% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<h1>Playoff Qualifiers</h1>
<div style="margin-left: 20px;">
<p><b>Unit Final (District Semi-Final) Game Schedule:</b></p>
<ul>
<li>Sunday, October 15, 10:00 a.m., South Bay Bridge Club</li>
<li>Sunday, November 5, 10:00 a.m., Long Beach Bridge Club</li>
</ul>
</div>
<h3><a href="/registration">Register here to play in a semi-final</a></h3>
<h3><a href="/clubgames">List of club games reported to date</a></h3>
<h3><a href="/summary">Summary of all qualified players</a></h3>

<h3>Qualifiers by individual club, game, or player</h3>
<div style="margin-left: 20px;">
<p>
<form method="get" action="/find/player">
<label>Enter player number: <input name="pnum" size="8"/></label>
<button>Submit</button>
</form>
</p>
<p>
<form method="get" action="/find/club">
<label>Select a club:
<select name="club_num" onchange="this.form.submit()">
  <option value="999" selected>Choose a club:</option>
% for club in clubs:
  <option value="{{club['num']}}">{{club['name']}}</option>
% end
</select>
</label>
</form>
</p>
<p>
<form method="get" action="/find/game">
<label>Select an individual game:
<select name="game_index" onchange="this.form.submit()"">
  <option value="999" selected>Choose a game:</option>
% for idx, g in enumerate(games):
  <option value="{{idx}}">{{g['name']}} {{g['date']}} {{g['session']}}</option>
% end
</select>
</label>
</form>
</p>
</div>
<h3>Club managers and directors: <a href="/submit_gamefile">Submit new game file</a></h3>
<p>&nbsp;</p>
<p><a href="/appnotes">Application notes here</a></p>
