<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{{title}}</title>
<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet"> 
<style>
body {
  font-family: 'Lato', sans-serif;
}
.headfoot a:link {
  color: #8ff
}
.headfoot a:visited {
  color: #fff
}
.headfoot a:hover {
  color: #0ff
}
.headfoot {
  color: #ddd;
  background-color: #008;
  padding: 10px;
  border: 0;
  margin: 0;
}
#top h1, #top h2, #top h3 {
  padding: 0;
  margin: 0;
  border: 0;
}
</style>
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
<div id="bottom" class="headfoot">
<p>Hosted by <a href="http://bridgemojo.com">BridgeMojo</a></p>
<p><a href="http://mail.bridgemojo.com/mailman/listinfo/napd23">Join the NAPD23 email list</a></p>
</div>
</div>
</body>
</html
