# Movies API

Project is hosted on heroku: https://shielded-wave-76701.herokuapp.com

To run the app locally please use local_setup branch that uses sqlite3 database.

## API endpoints:

### Movies
* Adds movie to database and return details. Required: ('title') 
  * POST https://shielded-wave-76701.herokuapp.com/movies
* Returns movies. Available filtering: genre, director, actor
  * GET https://shielded-wave-76701.herokuapp.com/movies
  * GET https://shielded-wave-76701.herokuapp.com/movies?genre=Drama&actor=Colin%20Farrell

### Comments
* Adds comment to the movie. Required: ('movie_id', 'body') 
  * POST https://shielded-wave-76701.herokuapp.com/comments 
* Returns comments. Available filtering: movie_id
  * GET https://shielded-wave-76701.herokuapp.com/comments?movie_id=3
  
### Top
* Returns ranking of top commented movies in date range. Required: from, to in date format.
  * GET https://shielded-wave-76701.herokuapp.com/top?from=2018-01-01&to=2019-03-19
