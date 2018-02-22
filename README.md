# Hack Oregon Transportation Systems Backend Repository

This repo represents the work of the Transportation Systems project of Hack Oregon. We are a volunteer project for Open Data.

This repo is intended to be run in a docker environment.

## A note about line endings
As you probably know, text files on Linux (where we deploy and where our containers run) have by convention lines ending with `LF`. However, Windows, where some of us test and develop, uses the convention that lines in a text file end with a `CR` and a `LF`.

Git knows what we're using, and it tries to accomodate us by checking out working files with the line endings our platform uses. See this explainer from GitHub on how line endings work with Git: <https://help.github.com/articles/dealing-with-line-endings/>.

Now, throw in Docker and Docker Compose. Some Dockerfiles call for copying files from your host into the image during the build. If those files came from a Git repo, the default is that their line endings are your host native convention. But inside the image, which is a Linux filesystem, some files must use the Linux line ending convention or they won't work.

So far, we know that Bash and `sh` scripts will crash if they have Windows line endings, often with mysterious error messages. Also, Python scripts like Django's `manage.py`, when executed as commands, will crash mysteriously if they have Windows line endings.

One final note: `vim` has a command `:setfileformat`. Either `:setfileformat unix` if you want the Unix / Linux convention or `:setfileformat dos` if you want the DOS / Windows convention. Then save the file and edit your `.gitattributes` file to declare that the file must have that convention on checkout.

## Restarting Docker for Windows sometimes necessary
Sometimes, Docker for Windows loses contact with some critical resource and throws ugly messages like this:

```
ERROR: for transportationsystembackend_db_1  Cannot start service db: driver failed programming external connectivity on endpoint transportationsystembackend_db_1 (f944aeb0244747359af77373b4949561c6e6e1d8ee48fb0bfc8aba98aa32877e): Error starting userland proxy: mkdir /port/tcp:0.0.0.0:5439:tcp:172.18.0.2:5432: input/output error

ERROR: for db  Cannot start service db: driver failed programming external connectivity on endpoint transportationsystembackend_db_1 (f944aeb0244747359af77373b4949561c6e6e1d8ee48fb0bfc8aba98aa32877e): Error starting userland proxy: mkdir /port/tcp:0.0.0.0:5439:tcp:172.18.0.2:5432: input/output error
Encountered errors while bringing up the project.
```

If this happens, you will need to restart Docker. Open the `Settings` dialog and go to `Reset`. Select the `Restart` option (the top one). Wait till the green `Docker is running` light shows up and then go back to your terminal. Everything should then work. ***This is a known Docker for Windows bug, not something you did wrong.***

## Getting Started

In order to run this you will want to:

1. Clone this Repository

2. `cd` into it

3. The environment variables that Docker uses and inserts into the images it builds are taken from a file in the root of this repository called `.env`. Because it contains sensitive information like passwords, it is not checked into version control - you have to create it as follows:

    * Copy `env.sample` to `.env`: `cp env.sample .env`
    * Edit `.env` and change at least `POSTGRES_PASSWORD` and `DJANGO_SECRET_KEY`. You should not need to change any of the others during test and development.

4. Download the database `.backup` files from Google Drive and place them in `./Backups` *before doing the Docker build.* The build will copy them onto the image and the first "run" in a container will restore them. See [Automatic database restores](https://github.com/hackoregon/data-science-pet-containers/blob/master/README.md#automatic-database-restores) for the details on the restore mechanism.

5. The `.env` file and the `.backup` files have been added to the `.gitignore` file. Provided you do not rename them or change locations they will not be committed to the repo and this project will build and run.

6. Confirm you have executable perms on all the scripts in the `./bin` folder: `$ chmod +x ./bin/*.sh` Feel free to read each one and assign perms individually, cause it is your computer :stuck_out_tongue_winking_eye: and security is a real thing.

7. Run the `build.sh` script to build the project. Since you are going to be running it on the local machine you will want to run: `./bin/build.sh -l` - This command is doing a docker-compose build in the background. It is downloading the images needed for the project to your local machine.

8. Once this completes you will now want to start up the project. We will use the start.sh script for this, again using the `-l` flag to run locally:  `./bin/start.sh -l` The first time you run this you will see the database restores. You can ignore the error messages. You will also see the api container start up.

9. Once the first startup completes kill the container using cmd c/ctrl c depending on your os.

10. Restart the container using the same start command:  `./bin/start.sh -l` and both the db and the api will start up.

11. Open your browser and you will be able to access the Django Rest Framework browserable front end at `http://localhost:8000/api`, the Swagger API schema at `http://localhost:8000/schema`, and the Django `admin` login at `http://localhost:8000/admin`.

12. To Run Tests: run the `./bin/build.sh -l` followed by the `./bin/test.sh -l`  command.

13. Note that the `api` container will write some files into your Git repository. They're in `.gitignore`, so they won't be checked into version control.

## Run in Staging Environment

While developing the API, using the built in dev server is useful as it allows for live reloading, and debug messages. When running in a production environment, this is a security risk, and not efficient. As such a staging/production environment has been created using the following technologies:

* [Gunicorn](http://gunicorn.org/) - A "green" HTTP server
* [Gevent](http://www.gevent.org/) - Asynchronous workers
* [Pyscopgreen](https://pypi.python.org/pypi/psycogreen) - A "green" version of the psycop database connector
* [django_db_geventpool](https://pypi.python.org/pypi/django-db-geventpool) -  DB pool using gevent for PostgreSQL DB.
* [WhiteNoise](https://pypi.python.org/pypi/whitenoise) - allows for hosting of static files by gunicorn in a prod environment vs. integrating a webserver

### Instructions:

1. copy the `/bin/env.staging.sample` file to create a `.env.staging` file in same directory:
```
$ cp ./bin/env.staging.sample ./bin/.env.staging
```

2. open the `./bin/.env` in your text editor and complete the environmental variables.

3. Download and save the sql file if you have not already.

4. Run the `build.sh` script to build the project for the staging environment: `$ ./bin/build.sh -s`

5. Start the project using the staging flag: `$ ./bin/start.sh -s`

6.  Open your browser and you should be able to access the Django Restframework browserable front end at: http://localhost:8000/api and Swagger at http://localhost:8000/schema

7. Try going to an nonexistent page and you should see a generic 404 Not found page instead of the Django debug screen.

### What was configured:

So what is changed from the default Django setup for the staging environment. **This already has been done, being included for informational purposes**

* Add gunicorn, gevent, and whitenoise to `requirements.txt`
* Set the debug variable to false in the `.env.staging`
* make any other changes necessary to config vars, ie: database settings
* create a staging entrypoint/prod entrypoint file that runs the gunicorn start command instead of the ./manage.py runserver
* create the `gunicorn_config.py` file to hold gunicorn config, including using gevent worker_class
* create a staging/production docker_compose file, to use the correct .env, entrypoint, and any other changes needed
* Make changes to settings.py:

```
# Change DEBUG line:

DEBUG = os.environ.get('DEBUG') == "True" - handles os variables being treated as strings

# ADD to MIDDLEWARE right after SECURITY:


'whitenoise.middleware.WhiteNoiseMiddleware',

# ADD these just before the STATIC_URL so staticfiles are handled correctly and are compressed:

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```


## Contributing

To develop on the repo,

1. Create an issue for tracking and communication

2. You will clone repo and then create a feature branch.

3. After branching confirm you can follow above get started steps.

4. Develop you feature

5. Update documentation and env sample file as necessary.

6. Commit Changes.

7. Merge current Staging branch into feature branch to resolve any merge conflicts.

8. Push local feature branch to Hack Oregon repo. Any PR requests from forks will be rejected.

9. Create a Pull Request to staging branch. No PRs will be accepted to Master unless from staging and by approved reviewers

10. PR should be reviewed by authorized reviewer, another team member if possible, and pass any automated testing requirements.

11. Any outstanding merge conflicts resolved

12. Authorized reviewer will commit to staging.

13. Process for staging to master will be defined.

## API

The primary function of this API is to act as a read-only wrapper around ODOT's Crash data and expose the underlying data to the web via HTTP Requests. The secondary function is eventually expose helper functions that could simplify data pre-processing via in-built helper functions. This API aims to be RESTful.

#### Note on Unmanaged models
The models in this project are unmanaged. Given that a) the API sits upon a legacy database and b) the API is intended to be read-only, the decision was made to decouple Django from database management and isolate that solely to the underlying PostGres shell environment. This is to prevent creation and deletions of the underlying data tables primarily during development. Malicious editing (outside of the dev environment) is less of a concern since that can be handled by a secure permissions for users making API calls.

### Note on Permissions
All users can browse the API. Read-only access is the default permission for unauthenticated users.

### Note on Testing
Testing an unmanaged model requires a few modifications to the test runner. Since migrations don't create any tables, they create a blank test database which results in no test data being found. The fix is outlined in the following post - https://dev.to/patrnk/testing-against-unmanaged-models-in-django

Runnning a test requires you have 'django-test-without-migrations' as part of your requirements. The only other point to remember is that tests need to be run with `./manage.py test --no-migrations` flag to prevent Django from trying to run migrations on your test db. 

### Endpoints
* API endpoints can viewed in a browser.
* List of endpoints (assuming local machine as hostm with port 8000 exposed):
  * *API Root* - http://localhost:8000/api/
  * *Schema* - http://localhost:8000/schema/
  * *Crashes Table* - http://localhost:8000/api/crashes/
  * *Participants Table* - http://localhost:8000/api/participants/
  * *Vehicles Table* - http://localhost:8000/api/vehicles/

### Crashes Table
TBD

### Participants Table
TBD

### Vehicles Table
TBD

### Filtering
Three types of filters are currently supported -

#### 1. Search Filters
Simple text search can be performed on the following fields:
##### Crash Table
```python
'crash_id','crash_hr_short_desc','urb_area_short_nm','fc_short_desc','hwy_compnt_short_desc','mlge_typ_short_desc', 'specl_jrsdct_short_desc','jrsdct_grp_long_desc','st_full_nm','isect_st_full_nm','rd_char_short_desc', 'isect_typ_short_desc','crash_typ_short_desc','collis_typ_short_desc','rd_cntl_med_desc','wthr_cond_short_desc','rd_surf_short_desc','lgt_cond_short_desc','traf_cntl_device_short_desc','invstg_agy_short_desc','crash_cause_1_short_desc','crash_cause_2_short_desc','crash_cause_3_short_desc','pop_rng_med_desc','rd_cntl_med_desc'
```
##### Participants Table
TBD
##### Vehicles Table
TBD
#### Usage:
To look for all fields listed above that match (not exact) the string "DIS-RAG" -
```
http://localhost:8000/api/crashes/?search=DIS--RAG
```

#### 2. Field Filters
The API also supports explicit filter fields as part of URL query strings. The following fields are currently supported -
```python
'ser_no','cnty_id','alchl_invlv_flg','crash_day_no','crash_mo_no','crash_yr_no','crash_hr_no','schl_zone_ind','wrk_zone_ind','alchl_invlv_flg','drug_invlv_flg','crash_speed_invlv_flg','crash_hit_run_flg'
```
##### Usage:
If filtering just "00173" and "00174" for the field 'ser_no' -
```
http://localhost:8000/api/crashes/?ser_no=00173&ser_no=00174
```

#### 3. Ordering Filters
Results can be sorted against any field or combinations of fields.
##### Usage:
To show results in ascending order of the field 'ser_no':
```
http://localhost:8000/api/crashes/?ordering=ser_no
```
In descending order:
```
http://localhost:8000/api/crashes/?ordering=-ser_no
```
multiple fields:
```
http://localhost:8000/api/crashes/?ordering=-ser_no,rd_cntl_med_desc
```


### Versions
The API supports Accept Header Versioning. Version numbers in API requests are optional and if no version is specified the request header _latest_ version is returned by default. Specify versions as numbers, as shown in header example below -

```
GET /api/crashes HTTP/1.1
Host: example.com:8000
Accept: application/json; version=1.0
```

__Latest__ version: 1.0 (as of 02/19/2018)


## License

We follow the MIT License: https://github.com/hackoregon/transportation-system-backend/blob/staging/LICENSE

## Contributors

<To Be added>
