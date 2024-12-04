Spotify API data in CSV format to be used in the DATA100 final Project. 


Update: The spotify API, during the devolopment of this project, has closed many of the endpoints that 
this projects code calls on.

This means that the code in the "dancibility.py" file, while correct and compilable, now returns http errors.
This rather unfortunate change means that the code is no longer able to run as intended.

In the all_songs and dancibility csv's, there is a column called "Added by". This column
represents the spotify user who added the song to the playlist. The reason for this column in all of the non "top 100" csv
files is due to the fact that the data we pulled more recently (i.e the data that is no longer acessible through spotify's 
web api) is being pulled through a by-user ios api, which has not yet closed the song metric endpoints. This creative temporary
workaround has allowed myself to gather important data at the expense of one additional redundant column (Which will
be removed druing the cleaning process anyway.)\

