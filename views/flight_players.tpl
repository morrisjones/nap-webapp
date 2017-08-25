% rebase('nap-frame.tpl')
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
  <td>{{fp['player_name']}}</td>
  <td>{{fp['player_number']}}</td>
  <td>
    {{qd[0].sdate}} <i>{{qd[0].club}}</i>
    % for i in range(1,len(qd)):
    <br/>{{qd[i].sdate}} <i>{{qd[i].club}}</i>
    % end
  </td>
% end
</table>
<p>&nbsp;</p>
<p><a href="/">Return to home page</a></p>
