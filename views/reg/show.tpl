% rebase('nap-frame.tpl',title='North American Pairs, District 23')
% from nap.prereg import Seat
<h2><a href="/registration/">Register for a semi-final game</a></h2>
<h2 style="color: blue;">Test data only, not actual reservations</h2>
% for uf in ('UF1','UF2'):
% if uf == 'UF1':
<h3>Unit Final 1 - South Bay Bridge Club Oct. 15 10:00 a.m.</h3>
% elif uf == 'UF2':
<h3>Unit Final 2 - Long Beach Bridge Club Nov. 5 10:00 a.m.</h3>
%end
% for flight in ('a','b','c'):
<h4>Flight {{flight.upper()}}</h4>
<table id="{{uf}}-{{flight}}">
<tr><th>&nbsp;</th><th>North-South</th><th>East-West</th></tr>
% section = reg[uf][flight]['section']
% max_table = reg[uf][flight]['max_table']
% for table_number in range(1,max_table+1):
<tr><td>Table {{table_number}}</td>
% for direction in (Seat.NS, Seat.EW):
<td>
% seat = reg[uf][flight]['section'][table_number][direction]['seat']
% if seat:
{{seat['player_a']['lname']}}, {{seat['player_a']['fname']}}<br/>
{{seat['player_b']['lname']}}, {{seat['player_b']['fname']}}
% else:
Available
% end
</td>
% end
</tr>
% end
</table>
% end