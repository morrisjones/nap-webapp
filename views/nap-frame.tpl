<!DOCTYPE html>
<html>
<%
from __version__ import __version__
version = __version__
%>
<head>
<meta charset="UTF-8">
<meta name=viewport content="width=500, initial-scale=0.8">
<title>{{title}}</title>
<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="/nap-webapp.css">
</head>
<body>
<div class="container">
  <div id="top" class="headfoot" 
  % if not defined('home'):
  onclick="document.location='/';return false;"
  % end
  >
    <h1>North American Pairs</h1>
    <h2>District 23, Los Angeles</h2>
    % if defined('home'):
    <h3><i>NAP Coordinator, Morris "Mojo" Jones, mojo@bridgemojo.com</i></h3>
    % end
  </div>
{{!base}}
% if not defined('home'):
<p>&nbsp;</p>
<p><a href="/">Return to home page</a></p>
% end
<div id="bottom" class="headfoot">
<p>
Hosted by <a href="http://bridgemojo.com">BridgeMojo</a><br/>
<a href="http://mail.bridgemojo.com/mailman/listinfo/napd23">Join the NAPD23 email list</a><br/>
Version {{version}}
</p>
</div>
</div>
</body>
</html
