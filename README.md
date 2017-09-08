North American Pairs District 23
================================

https://nap.bridgemojo.com

This app is currently serving ACBL District 23 for the North American Pairs
tournament. There are two main use cases:

1. Enable uploading and reporting of players from designated NAP club games
who qualify to advance to the next round of playoffs.

   Club managers and directors can upload ACBLscore game files directly to
the app to report their qualifier lists.

   Players and interested parties can see the list of qualified players in
a number of different formats.

   Files can be uploaded both as ACBLscore game files, or as an NAP report CSV
file. Advantage goes to game file uploads, as the app is able to report
table count, game date and session, and other valuable information.

2. Accept reservations for games in the next round of playoffs.

   A partnership may use the site to announce their intention to play in one
of the Unit Final games (the district semi-final).

   The partnership providesa contact email address. An email is sent to that
address with a confirmation link. After clicking on the link from the
email, the partnership is assigned a provisional table.

   At the tournament, entry slips will be available for all preregistered
partnerships, and they will pay a slightly discounted fee.

Implementation and deployment
-----------------------------

Nap-webapp is deployed on a Linode virtual machine running CentOS 7.

The front-end http server is NGINX, and the middleware is uwsgi.

The web framework is Bottle, https://bottlepy.org

Basic data services are provided by the companion Python module nap,
which handles data processing of game files.

There is no back end storage database! The fundamental storage is in
disk files.

Memcached provides in-memory storage of the NAP data as JSON objects
to avoid frequent processing of the ACBLscore game files.

Configuration variables:

MEMCACHED  
hostname:port for memcached (localhost:11211)

LOG_LEVEL  
One of INFO DEBUG WARNING ERROR CRITICAL

LOG_FILE  
Suggest /var/log/nap.bridgemojo.com.log

GAMEFILE_TREE  
Root directory of a tree of game files from qualifier games, must be read/write
for the user running the app (for instance uwsgi).

GAMEFILE_UPLOADS  
Root directory where new game file uploads land for processing, must be read/write
for the user running the app (uwsgi)

UNIT_REGISTRATION  
Root directory where registrations and confirmations are persisted, must be
read/write for the user running the app (uwsgi).

MAIL_HOST  
Host name of the SMTP server (mail.rs.whiteoaks.com)

MAIL_USER  
User name for the mail server

MAIL_PASSWORD  
Password for the mail server


