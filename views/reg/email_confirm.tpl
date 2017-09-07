% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<h2>Email confirmation link</h2>
% if error_messages:
% for msg in error_messages:
<h3 style="color: red;">{{msg}}</h3>
% end
<h3><i>Please try again or <a href="mailto:nap@bridgemojo.com">contact Mojo for help</a></i></h3>
% else:
<h3>Congratulations! Reservation confirmed</h3>
<table>
<tr><td><b>Player</b></td><td>{{player_a}}<br/>{{pnum_a}}</td></tr>
<tr><td><b>Player</b></td><td>{{player_b}}<br/>{{pnum_b}}</td></tr>
<tr><td><b>Game</b></td><td>{{game_desc}}</td></tr>
<tr><td><b>Flight</b></td><td>{{flight_desc}}</td></tr>
<tr><td><b>Require N/S</b></td><td>{{"Yes" if bool(req_ns) else "No"}}</td></tr>
<tr><td><b>Confirmation email</b></td><td>{{email}}</td></tr>
<tr><td><b>(Provisional) Table No.</b></td><td>{{table_number}} {{direction}}</td></tr>
</table>
% end
<h3><a href="/registration/show">Click here to see current reservations</a></h3>

