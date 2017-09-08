% rebase('nap-frame.tpl')
<table id="clubgames">
<h2>Total games: {{total_games}}<br/>
Total tables: {{total_tables}}</h2>
<tr>
  <th>Club No.</th>
  <th>Club Name</th>
  <th>Date</th>
  <th>Session</th>
  <th>Tables</th>
</tr>
% for row, cg in enumerate(club_games):
% bgclass = ("odd" if ((row % 2) == 1) else "even")
<tr class="{{bgclass}}">
  <td>{{cg['club_number']}}</td>
  <td>
  <a href="/find/club?club_num={{cg['club_number']}}">
  {{cg['club_name']}}
  </a>
  </td>
  <td>
    <a href="find/game?game_index={{cg['game_index']}}">
    {{cg['game_date']}}
    </a>
  </td>
  <td>{{cg['session_name']}}</td>
  <td style="text-align: right">{{cg['tables']}}</td>
</tr>
% end
</table>
% if flight_totals and players:
% include('summary',flight_totals=flight_totals,players=players)
% end
