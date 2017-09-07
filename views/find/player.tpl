% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<h1>Find Player</h1>
% if error_msg:
<h2>{{pnum}}: {{error_msg}}</h2>
% else:
<h2>{{name}}</h2>
<p>
Player number: {{pnum}}<br/>
Qualifiers: {{flta}} {{fltb}} {{fltc}}<br/>
Qualifier game dates:<br/>
<table>
<tr>
  <th>Game date</th>
  <th>Club</th>
</tr>
% for qd in qualdates:
<tr>
  <td>{{qd.date}}</td>
  <td>{{qd.club.name}}</td>
</tr>
% end
</table>
% end
