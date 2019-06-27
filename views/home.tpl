% rebase('nap-frame.tpl',title='North American Pairs, District 23')

<!-- OLD Unit Final and District Final schedule

<h3><a href="https://results.bridgemojo.com/unit-final/">Unit Final Results</a></h3>

<h3><a href="/unit-final-summary">Summary of District Final Qualifiers</a></h3>

-->

<h2>2019 Unit and District Playoff Games</h2>
<div style="margin-left: 20px;">
<p><b>Unit Final Game Schedule:</b></p>
<ul>
<li>Sunday, September 15, 10:00 a.m., Long Beach Bridge Club</li>
<li>Sunday, October 20, 10:00 a.m., San Marino Bridge Club, 1800 Huntington Drive</li>
</ul>
<p><b>District Final</b></p>
<ul>
<li>Sunday, November 17, 10:00 a.m., South Bay Bridge Club, Lomita</li>
</ul>
<p><b>National Final</b></p>
<ul>
<li><a href="https://nabc.acbl.org/upcoming-nabc/">Colubmus, Ohio, NABC, March 19-29</a></li>
</ul>
</div>

<!-- Registration for Unit Final Games

<h3><a href="/registration">Register here to play in a semi-final</a></h3>
<h3><a href="/registration/show">See current attendance at the Unit Final</a></h3>
<h3><a href="/unit-final-flier-2018-19.pdf">Click here for the Unit Final flier PDF</a></h3>

-->

<h2>NAP 2019-20 Conditions of Contest</h2>

<h3><a href="http://web2.acbl.org/documentLibrary/play/NAP/CoC.pdf">Click here</a> for the national CoC</h3>

<h2>Results compiled from club qualifying games</h2>

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
<select name="game_index" onchange="this.form.submit();">
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
