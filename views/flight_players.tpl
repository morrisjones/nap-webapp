% rebase('nap-frame.tpl')
<h2>Total eligible: {{len(flight_players)}}</h2>
<table id="flight">
<tr>
  <th>Name</th>
  <th>Player No.</th>
  <th>Qualifying games</th>
</tr>
% for row, fp in enumerate(flight_players):
% bgclass = ("odd" if ((row % 2) == 1) else "even")
% qd = fp['qualdates']
<tr class="{{bgclass}}">
  <td><a href="/findplayer?pnum={{fp['player_number']}}">{{fp['player_name']}}</a></td>
  <td><a href="/findplayer?pnum={{fp['player_number']}}">{{fp['player_number']}}</a></td>
  <td>
    {{qd[0].sdate}} <i>{{qd[0].club}}</i>
    % for i in range(1,len(qd)):
    <br/>{{qd[i].sdate}} <i>{{qd[i].club}}</i>
    % end
  </td>
% end
</table>
