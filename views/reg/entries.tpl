% from nap.prereg import Seat
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">
<title>Game Entries</title>
<style>
body {
  font-family: 'Lato', sans-serif;
}
.entry table {
    width: 100%;
}
.entry th, td {
    border: 0;
}
.reflist table {
    width: 99%;
    border-collapse: collapse;
}
.reflist td {
    border: 1px black solid;
    border-collapse: collapse;
}
.entry td h1 {
    vertical-align: middle;
    text-align: center;
}
div.entry {
    page-break-inside: avoid;
}
div.reflist {
    page-break-inside: avoid;
}
</style>
</head>
<body>

<h1>Entry List for {{game}}</h1>
% for flight in ('a','b','c'):
% section = reg[flight]['section']
% max_table = reg[flight]['max_table']
<div class="reflist">
<h2>Flight {{flight.upper()}}</h2>
<table>
<tr><th colspan="2">Players</th><th>Seat</th><th>Require N/S</th></tr>
% for table in range(1,max_table+1):
% for direction in (Seat.NS,Seat.EW):
% seat = reg[flight]['section'][table][direction]['seat']
% if seat:
<tr>
<td>{{seat['player_a']['lname']}}, {{seat['player_a']['fname']}} {{seat['player_a']['pnum']}}</td>
<td>{{seat['player_b']['lname']}}, {{seat['player_b']['fname']}} {{seat['player_b']['pnum']}}</td>
<td>{{table}} {{direction}}</td>
<td style="text-align: center;">
% if seat['req_ns']:
<span style="background-color: yellow;"><b>Yes</b></span>
% else:
&nbsp;
% end
</td>
</tr>
% end
% end
% end
</table>
</div>
% end
<hr style="page-break-after: always;"/>

% for flight in ('a','b','c'):
% section = reg[flight]['section']
% max_table = reg[flight]['max_table']
% for table in range(1,max_table+1):
% for direction in (Seat.NS,Seat.EW):
% seat = reg[flight]['section'][table][direction]['seat']
% if seat:
<div class="entry">
<h1>North American Pairs District 23</h1>
<h2>Unit Final &mdash; {{game}}</h2>
<table>
<tr><th style="width: 40%">Pair Entry</th><th>Section</th><th>Table</th><th>Direction</th><tr>
<tr><td>
<p>
{{seat['player_a']['fname']}} {{seat['player_a']['lname']}}<br/>
{{seat['player_a']['pnum']}}
</p>
<p>
{{seat['player_b']['fname']}} {{seat['player_b']['lname']}}<br/>
{{seat['player_b']['pnum']}}
</p>
% if seat['req_ns']:
<p style="background-color: yellow;">
<i>Requires stationary N/S</i>
% else:
<p>
&nbsp;
% end
</p>
</td>
<td><h1>{{flight.upper()}}</h1></td>
<td><h1>{{table}}</h1></td>
<td><h1>{{direction}}</h1></td></tr>
</table>
<hr style="width: 90%;"/>
</div>
% end
% end
% end
% end
</body>
</html>