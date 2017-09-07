% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<%
if game == 'UF1':
  game_desc = "Oct. 15, South Bay Bridge Club, 10:00 a.m."
elif game == 'UF2':
  game_desc = "Nov. 5, Long Beach Bridge Club, 10:00 a.m."
else:
  game = "Error, bad game code: '%s'" % game
end
if flight == 'a':
  flight_desc = "A (Open)"
elif flight == 'b':
  flight_desc = "B (0-2500)"
elif flight == 'c':
  flight_desc = "C (Non-Life Master 0-500)"
else:
  flight_desc = "Error unknown flight: '%s'" % flight
end
%>
<h2>Confirm game reservation</h2>

<table>
<tr><td><b>Player</b></td><td>{{player_a}}<br/>{{pnum_a}}</td></tr>
<tr><td><b>Player</b></td><td>{{player_b}}<br/>{{pnum_b}}</td></tr>
<tr><td><b>Game</b></td><td>{{game_desc}}</td></tr>
<tr><td><b>Flight</b></td><td>{{flight_desc}}</td></tr>
<tr><td><b>Require N/S</b></td><td>{{"Yes" if bool(req_ns) else "No"}}</td></tr>
<tr><td><b>Confirmation email</b></td><td>{{email}}</td></tr>
</table>

<form method="post" action="confirm">
<input type="hidden" name="game" value="{{game}}">
<input type="hidden" name="flight" value="{{flight}}">
<input type="hidden" name="player_a" value="{{player_a}}">
<input type="hidden" name="pnum_a" value="{{pnum_a}}">
<input type="hidden" name="player_b" value="{{player_b}}">
<input type="hidden" name="pnum_b" value="{{pnum_b}}">
<input type="hidden" name="req_ns" value="{{req_ns}}">
<input type="hidden" name="email" value="{{email}}">
<h2>Send confirmation email?</h2>
<p>An email will be sent to the address you provided with a link that will make this reservation final.
</p>
<p>
<input name="confirm" type="radio" value="yes" checked/>Yes<br/>
<input name="confirm" type="radio" value="no"/>No, discard this reservation<br/>
</p>
<p><button>Submit</button></p>
</form>