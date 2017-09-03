% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<h1>Playoff Qualifiers</h1>
<h3><a href="/clubgames">List of club games reported to date</a></h3>
<h3><a href="/summary">Summary of all qualified players</a></h3>
<h3>Players by flight, with qualifying games:<br/>
<a href="/flta">Flight A</a>
<a href="/fltb">Flight B</a>
<a href="/fltc">Flight C</a></h3>
<h3>Result by individual club, game, or player</h3>
<div style="margin-left: 20px;">
<p>
<form method="get" action="/findplayer">
<label>Enter player number: <input name="pnum" size="8"/></label>
<button>Submit</button>
</form>
</p>
<p>
<form method="get" action="/findclub">
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
<form method="get" action="/findgame">
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
