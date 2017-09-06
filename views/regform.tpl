% # See here:
% # https://stackoverflow.com/questions/29882361/show-datalist-labels-but-submit-the-actual-value
% rebase('nap-frame.tpl',title='North American Pairs, District 23')

<h1>District 23 Semi-Final Games</h1>
<h2>Register to play</h2>

<p>Select a semi-final game to play. All contestants must be members in
good standing with ACBL.
</p>

<p><b>Note:</b> <i>You may only play in one semi-final (Unit Final) game.</i>
</p>

% if defined('error_messages'):
% for msg in error_messages:
<h3 style="color: red;">
{{msg}}
</h3>
% end
<h3><i>Please try again or contact <a href="mailto:mojo@whiteoaks.com">Mojo</a></i></h3>
% end

<datalist id="playerlist">
% for pnum in players:
  <option value="{{pnum}} | {{players[pnum]}}">{{players[pnum]}}</option>
% end
</datalist>

<form method="POST" action="/submit_regform">
<p><label><h3>Choose which game:<br/>
<select name="game">
<option value="UF2">Long Beach Bridge Club, November 5, 10:00 a.m.</option>
<option value="UF1">South Bay Bridge Club, October 15, 10:00 a.m.</option>
</select>
</h3></label>
</p>
<p><label><h3>Choose flight:<br/>
<select name="flight">
% flight = get('flight', 'a')
<option value="a" {{'selected' if flight == 'a' else ''}}>Flight A (Open)</option>
<option value="b" {{'selected' if flight == 'b' else ''}}>Flight B 0-2500</option>
<option value="c" {{'selected' if flight == 'c' else ''}}>Flight C Non-Life Master 0-500</option>
</select>
</h3></label></p>
<h3>Player 1:</h3>
<p>
<input list="playerlist" name="player_a" size="50" placeholder="Last name, First name ...">
</p>
<h3>Player 2:</h3>
<p>
<input list="playerlist" name="player_b" size="50" placeholder="Last name, First name ...">
</p>
<p>
<label>
% req_ns = get('req_ns', False)
<input type="checkbox" name="req_ns" {{'checked' if req_ns else ''}}/>
Check here you require a N/S seat for both sessions.
</label>
</p>
<p><button>Submit request</button></p>
</form>