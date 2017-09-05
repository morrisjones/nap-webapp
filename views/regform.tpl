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
<table class="noborder">
<tr>
<td class="noborder"><label>First name:<br/><input name="a_fname" value="{{get('a_fname','')}}"/><label></td>
<td class="noborder"><label>Last name:<br/><input name="a_lname" value="{{get('a_lname','')}}"/><label></td>
<td class="noborder"><label>ACBL Player No.:<br/><input name="a_pnum" value="{{get('a_pnum','')}}"/><label></td>
</tr>
</table>
</p>
<h3>Player 2:</h3>
<p>
<table class="noborder">
<tr>
<td class="noborder"><label>First name:<br/><input name="b_fname" value="{{get('b_fname','')}}"/><label></td>
<td class="noborder"><label>Last name:<br/><input name="b_lname" value="{{get('b_lname','')}}"/><label></td>
<td class="noborder"><label>ACBL Player No.:<br/><input name="b_pnum" value="{{get('b_pnum','')}}"/><label></td>
</tr>
</table>
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