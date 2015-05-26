# Chipy Mentorship Program

Brian and I are working on a project where we analyze the career earnings for all players currently ranked in the ATP
(Men's Professional Tennis Association) and examine correlations with the latest [Good Country Index](http://www.goodcountry.org/overall) 
and [Country Transparency Index](http://www.transparency.org/research/cpi/overview).

In order to be ranked, a player must compete professionally at least once in a calendar year.

The ATP releases weekly rankings: www.atpworldtour.com/Rankings/

Each player in the ranking list has his own clickable URL. The script fetches the whole list and iterates over each of
the players, using the URL to fetch the following common data points: Ranking #, First Name, Last Name, Country, Career-Prize-Money.

These data points are the common denominator for all players.


