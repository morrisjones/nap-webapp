% rebase('nap-frame.tpl',title='North American Pairs, District 23')
<script>
% # See here:
% # https://stackoverflow.com/questions/29882361/show-datalist-labels-but-submit-the-actual-value
function fillPnum(e) {
    var input = e,
        list = input.getAttribute('list'),
        options = document.querySelectorAll('#' + list + ' option'),
        hiddenInput = document.getElementById(input.id + '-hidden'),
        inputValue = input.value;

    hiddenInput.value = inputValue;

    for(var i = 0; i < options.length; i++) {
        var option = options[i];

        if(option.innerText === inputValue) {
            hiddenInput.value = option.getAttribute('data-value');
            break;
        }
    }
};
</script>
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
<h3><i>Please try again or <a href="mailto:nap@bridgemojo.com">contact Mojo for help</a></i></h3>
% end
<p>Players qualified: {{len(players.keys())}}</p>
<datalist id="playerlist">
% for pnum in players:
  <option data-value="{{pnum}}">{{players[pnum]}}</option>
% end
</datalist>

<form method="POST" action="/registration/register">
<p><label><h3 style="margin-bottom: 0;">Choose which game:</h3><br/>
<select name="game">
<option value="UF1" {{'selected' if game == 'UF1' else ''}}>South Bay Bridge Club, October 15, 10:00 a.m.</option>
<option value="UF2" {{'selected' if game == 'UF2' else ''}}>Long Beach Bridge Club, November 5, 10:00 a.m.</option>
</select>
</h3></label>
</p>
<p><label><h3 style="margin-bottom: 0;">Choose flight:</h3><br/>
<select name="flight">
% flight = get('flight', 'a')
<option value="a" {{'selected' if flight == 'a' else ''}}>Flight A (Open)</option>
<option value="b" {{'selected' if flight == 'b' else ''}}>Flight B 0-2500</option>
<option value="c" {{'selected' if flight == 'c' else ''}}>Flight C Non-Life Master 0-500</option>
</select>
</h3></label></p>
<h3>Player 1:</h3>
<p>
<input value="{{player_a}}" oninput="fillPnum(this);" id="plra" list="playerlist" name="player_a" size="50" placeholder="Last name, First name ...">
<input value="{{pnum_a}}" type="hidden" name="pnum_a" id="plra-hidden">
</p>
<h3>Player 2:</h3>
<p>
<input value="{{player_b}}" oninput="fillPnum(this);" id="plrb" list="playerlist" name="player_b" size="50" placeholder="Last name, First name ...">
<input value="{{pnum_b}}" type="hidden" name="pnum_b" id="plrb-hidden">
</p>
<h3>Confirmation Email Address</h3>
<p><label>This email address will be the contact point for the partnership:<br/>
<input size="40" value="{{email}}"" type="email" name="email" placeholder="Email address..."></label>
</p>
<p>
<label>
% req_ns = get('req_ns', False)
<input type="checkbox" name="req_ns" {{'checked' if req_ns else ''}}/>
Check here you require a N/S seat for both sessions.
</label>
</p>
<h3>Are you a robot?</h3>
<p><label>If not, type "bridge" in this box:
<input type="text" name="human">
</label>
</p>
<p><button class="button large-btn">Submit request</button></p>
</form>
