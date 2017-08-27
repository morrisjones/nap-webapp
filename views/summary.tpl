<table id="clubgames">
<h2>Total players: {{total_players}}<br/>
Flight A: {{flight_totals['a']}}<br/>
Flight B: {{flight_totals['b']}}<br/>
Flight C: {{flight_totals['c']}}<br/>
</h2>
<tr>
  <th>Name</th>
  <th>Player No.</th>
  <th>Flt A</th>
  <th>Flt B</th>
  <th>Flt C</th>
</tr>
% for row, player in enumerate(players):
% bgclass = ("odd" if ((row % 2) == 1) else "even")
% # bgclass="table_row"
<tr class="{{bgclass}}">
  <td><a href="/findplayer?pnum={{player['pnum']}}">{{player['name']}}</a></td>
  <td><a href="/findplayer?pnum={{player['pnum']}}">{{player['pnum']}}</a></td>
  <td style="text-align: center;">{{player['flta']}}</td>
  <td style="text-align: center;">{{player['fltb']}}</td>
  <td style="text-align: center;">{{player['fltc']}}</td>
</tr>
% end
</table>
