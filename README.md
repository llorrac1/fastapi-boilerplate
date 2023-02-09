# FastAPI Boilerplate
A boilerplate FastAPI app ready to deploy to Google Cloud with Redis and Sqlite support. 

By default, this boilerplate uses Sqlite via sqlmodel for a DB and also supports Redis via RedisOM. 

Ready to deploy on GCP via cloud run. 

Thanks to [@tiangolo](https://github.com/tiangolo/) for their incredible work on FastAPI and SQLModel. 


# Running and deploying
### To Run
From your terminal
1. Clone this repo `git clone https://github.com/llorrac1/fastapi-boilerplate` 
2. cd into fastapi-boilerplate `cd fastapi-boilerplate`
2. Install the requirements via your preferred method and set up a virtual env. I use pipenv, which mangages both via `pipenv install -r requirements.txt` (you'll need to install pipenv separately for this)
3. Activate the virtual env. With pipenv `pipenv shell`
4. Run the app `uvicorn app.main:app --reload`

### < To deploy on Google Cloud Run - WIP >

# Need help? 
### Fast API Docs -> https://sqlmodel.tiangolo.com/ 
### SQLModel Docs -> https://fastapi.tiangolo.com/ 
### RedisOM Docs -> https://github.com/redis/redis-om-python
### Sqlite Docs -> https://docs.python.org/3/library/sqlite3.html 
