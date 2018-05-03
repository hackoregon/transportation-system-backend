# Hack Oregon Transportation Systems Backend Repository

This repo represents the work of the Transportation Systems project of Hack Oregon. We are a volunteer project for Open Data.

This repo is intended to be run in a docker environment.

## Getting Started

In order to run this you will want to:

1. Clone this Repository

2. `cd` into it

3. The environment variables that Docker uses and inserts into the images it builds are taken from a file in the root of this repository called `.env`. Because it contains sensitive information like passwords, it is not checked into version control - you have to create it as follows:

    * Copy `env.sample` to `.env`: `cp env.sample .env`
    * Edit `.env` and change at least `POSTGRES_PASSWORD` and `DJANGO_SECRET_KEY`. You should not need to change any of the others during test and development.

4. Download the database `.backup` files from Google Drive or S3 and place them in `./Backups` *before doing the Docker build.* The build will copy them onto the image and the first "run" in a container will restore them. See [Automatic database restores](https://github.com/hackoregon/data-science-pet-containers/blob/master/README.md#automatic-database-restores) for the details on the restore mechanism. If you are not sure where to locate the database backup, you will want to talk to the Data Manager for the team, currently @brian.grant on slack or brian@hackoregon.org.

5. The `.env` file and the `.backup` files have been added to the `.gitignore` file. Provided you do not rename them or change locations they will not be committed to the repo and this project will build and run.

6. Confirm you have executable perms on all the scripts in the `./bin` folder: `$ chmod +x ./bin/*.sh` Feel free to read each one and assign perms individually, cause it is your computer :stuck_out_tongue_winking_eye: and security is a real thing.

7. Run the `build.sh` script to build the project. Since you are going to be running it for the development environment you will want to run: `./bin/build.sh -d` - This command is doing a docker-compose build in the background. It is downloading the images needed for the project to your local machine.

8. Once this completes you will now want to start up the project. We will use the start.sh script for this, again using the `-d` flag to run locally:  `./bin/start.sh -d`. The first time you run this you will see the database restores. It will take a minute or two to load. Once complete you should see output something like this:

```
api_development_1  | May 01, 2018 - 23:25:58
api_development_1  | Django version 2.0.1, using settings 'crash_data_api.settings'
api_development_1  | Starting development server at http://0.0.0.0:8000/
api_development_1  | Quit the server with CONTROL-C.
```

9. Open your browser and you will be able to access the Django Rest Framework browserable front end at `http://localhost:8000/api`, the Swagger API schema at `http://localhost:8000/schema`, and the Django `admin` login at `http://localhost:8000/admin`.

10. To Run Tests: run the `./bin/build.sh -d` followed by the `./bin/test.sh -d`  command.

11. Note that the `api_development` container will write some files into your Git repository. They're in `.gitignore`, so they won't be checked into version control.

## API

The primary function of this API is to act as a read-only wrapper around ODOT's Crash data and expose the underlying data to the web via HTTP Requests. The secondary function is eventually expose helper functions that could simplify data pre-processing via in-built helper functions. This API aims to be RESTful.

### Datasource

For information about the process used to input and process the data exposed in this API, take a look at the [Hack Oregon - Crash Data Wrangling](https://github.com/hackoregon/crash-data-wrangling) project repo.

#### Note on Unmanaged models
The models in this project are unmanaged. Given that a) the API sits upon a legacy database and b) the API is intended to be read-only, the decision was made to decouple Django from database management and isolate that solely to the underlying PostGres shell environment. This is to prevent creation and deletions of the underlying data tables primarily during development. Malicious editing (outside of the dev environment) is less of a concern since that can be handled by a secure permissions for users making API calls.

### Note on Permissions
All users can browse the API. Read-only access is the default permission for unauthenticated users.

### Note on Testing
We are using py.test to run tests. Do to current constraints on our architecture, and the read-only nature of our API, we are currently testing against the production and development databases.  

To run tests:

1. Run command `./bin/test.sh -d` or `./bin/test.sh -p` for the correct environment.
2. If you need to configure any test details:

* pytest.ini
* conftest.py

Checkout the [py.test](https://pytest-django.readthedocs.io/en/latest/tutorial.html) documentation for more information.

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
Note:

1. Filters need to be an exact match.
2. URLs need to be encoded. All reserved characters characters should be escaped. For example, a query on the field public_location_description with the value SW 6th & Salmon, then the query should look like this - http://localhost:8000/api/passenger-census/?public_location_description=SW%206th%20%26%20Salmon. Here both spaces (%20) and ampersands (%26) have been escaped.

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



## Run in a Production Environment

While developing the API, using the built in dev server is useful as it allows for live reloading, and debug messages. When running in a production environment, this is a security risk, and not efficient.

* https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
* https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment

As such a production environment has been configured to be run when using the build.sh -p and start.sh -p commands.

### A quick summary of python packages and why they are in there:

* Gunicorn - A "green" HTTP server - http://gunicorn.org/
* Gevent - Asynchronous workers - http://www.gevent.org/
* Pyscopgreen - A "green" version of the psycop database connector - https://pypi.org/project/psycogreen/
* django_db_geventpool - DB pool using gevent for PostgreSQL DB. - https://github.com/jneight/django-db-geventpool/tree/master/django_db_geventpool
* WhiteNoise - allows for hosting of static files by gunicorn in a prod environment vs. integrating a webserver - http://whitenoise.evans.io/en/stable/

This provides a fairly stable, often used stack for django deployment, basically staying within python for the bulk of our tools, and cutting out the need for a separate server for the swagger/browsable front end

### To start it:

1. Configure the PRODUCTION_ variables in the .env file (Ask the Team's Data Manager to get these. They will need to match the production or staging server). The idea here is that you will now be connecting to a live database environment an AWS or otherwise externally hosted and not running the local database container. (see below for additional details)

2. Run the build.sh script to build the project for the production environment: $ ./bin/build.sh -p

3. Start the project using the production flag: $ ./bin/start.sh -p

4. Open your browser and you should be able to access the Django Restframework browserable front end at: http://localhost:8000/api and Swagger at http://localhost:8000/schema

5. Try going to an nonexistent page and you should see a generic `404 Not Found` page instead of the Django debug screen.

### What was configured:

So this is what has been configured between various files:

* Add gunicorn, gevent, and whitenoise, django-db-geventpool, to requirements/production.txt
* Set the debug variable to false in the the production-docker-compose file
* make any other changes necessary to config vars, ie: database settings
* create a prod entrypoint file that runs the gunicorn start command instead of the ./manage.py runserver. Here is an example:

```
gunicorn crash_data_api.wsgi -c gunicorn_config.py
```

* create the gunicorn_config.py file to hold gunicorn config, including using gevent worker_class.

Currently we are patching psycopg2 and django with gevent/psycogreen in the post_fork worker. Also using 4 workers (which maybe too many?):

```
try:
    # fail 'successfully' if either of these modules aren't installed
    from gevent import monkey
    from psycogreen.gevent import patch_psycopg


    # setting this inside the 'try' ensures that we only
    # activate the gevent worker pool if we have gevent installed
    worker_class = 'gevent'
    workers = 4
    # this ensures forked processes are patched with gevent/gevent-psycopg2
    def do_post_fork(server, worker):
        monkey.patch_all()
        patch_psycopg()

        # you should see this text in your gunicorn logs if it was successful
        worker.log.info("Made Psycopg2 Green")

    post_fork = do_post_fork
except ImportError:
    pass
```
* Changed the settings.py file to use django_db_geventpool when in production mode. You will add this after the current database settings.:

```
if os.environ.get('DEBUG') == "False":

    DATABASES = {
        'default': {
            'ENGINE': 'django_db_geventpool.backends.postgis',
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': os.environ.get('POSTGRES_PORT'),
            'CONN_MAX_AGE': 0,
            'OPTIONS': {
                'MAX_CONNS': 20
            }
        }
    }
```

* create a staging/production docker_compose file, using correct env vars, entrypoint command, and removing the database container:

```
version: '3.4'
services:
  api_production:
    build:
      context: .
      dockerfile: DOCKERFILE.api.production
    image: api_production
    command: ./bin/production-docker-entrypoint.sh
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - PROJECT_NAME
      - DEBUG=False
      - POSTGRES_USER=${PRODUCTION_POSTGRES_USER}
      - POSTGRES_NAME=${PRODUCTION_POSTGRES_NAME}
      - POSTGRES_HOST=${PRODUCTION_POSTGRES_HOST}
      - POSTGRES_PORT=${PRODUCTION_POSTGRES_PORT}
      - POSTGRES_PASSWORD=${PRODUCTION_POSTGRES_PASSWORD}
      - DJANGO_SECRET_KEY=${PRODUCTION_DJANGO_SECRET_KEY}
```

* Make changes to `settings.py` to check the debug variable and use :

Change DEBUG line:
```
DEBUG = os.environ.get('DEBUG') == "True" - handles os variables being treated as strings
```
ADD to MIDDLEWARE right after SECURITY:

```
'whitenoise.middleware.WhiteNoiseMiddleware',
```

ADD these just before the STATIC_URL so staticfiles are handled correctly and are compressed:

```
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

## Travis

Travis is a Continuous Integration and Development tool which integrates with Github. It allows us to push code to Github and automatically run tests. Provided these tests pass, code will automatically be pushed to AWS and staging/production servers once the PR has been accepted and merged.

Checkout our Travis build logs here:

* https://travis-ci.org/hackoregon/transportation-system-backend

## License

We follow the MIT License: https://github.com/hackoregon/transportation-system-backend/blob/staging/LICENSE

## Contributors

<To Be added>
