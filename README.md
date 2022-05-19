# Users-Python-Flask
Project of a REST API for users management using Python and Flask.

# Usage
In order to run this API locally you need to have Docker running and change the 
last two lines of the .env file like follows (this changes the database_url from 
heroku-postgres to the postgres that Docker will build and run):
```
# DATABASE_URL='postgres://gzagrmwfbpnwfq:b185af0b182b933c4a14a7bb94c35cc9e58d1d46fe75f37cc2eeb87d4d325f29@ec2-44-194-117-205.compute-1.amazonaws.com:5432/dbdflgq12q1tkb'
DATABASE_URL='postgres://postgres:postgres@database:5432/database'
```

Then and run the following command to start the server and database
```
docker-compose build && docker-compose up
```

And now you can test all the routes.