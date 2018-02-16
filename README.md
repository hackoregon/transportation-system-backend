# Hack Oregon Transportation Systems Backend Repository

This repo represents the work of the Transportation Systems project of Hack Oregon. We are a volunteer project for Open Data.

This repo is intended to be run in a docker environment.

## Getting Started

In order to run this you will want to:

1. Clone this Repository

2. `cd` into it

3. copy the `env.sample` file to `.env`:
```
$ cp env.sample .env
```

4. open the `.env` in your text editor and complete the environmental variables. When working in your dev. environment, only the prefilled ones really matter. If you are working as part of the project team we will discuss any need for standardization or other environments in team setting.

    Annotated sample:

    ```
    PROJECT_NAME=<This will be our canonical project name once it is figured out>
    DEBUG=True - <Switch to go from dev server environment to prod>
    POSTGRES_USER= <User in postgres environment>
    POSTGRES_NAME=odot_crash_data <Database name in postgres environment set to odot_crash_data for current dataset>
    POSTGRES_HOST=db <connects to database container name in the docker compose file>
    POSTGRES_PORT= <port for the database>
    POSTGRES_PASSWORD= <password, make it strong and unique>
    DJANGO_SECRET_KEY= <a secret key also should be long, unique random string>
    ```
5. This release features automatic database restores to the `db` database service container. You can create database backups with `pgAdmin` or `pg_dump` and place them in `./Backups` *before doing the Docker build.* The build will copy them onto the image and the first "run" in a container will restore them. See [Automatic database restores](https://github.com/hackoregon/data-science-pet-containers/blob/master/README.md#automatic-database-restores)

6. The `.env` file and the backup files have been added to the `.gitignore` file. Provided you do not rename them or change locations they will not be committed to the repo and this project will build and run.

7. Confirm you have executable perms on all the scripts in the `./bin` folder: `$ chmod +x ./bin/*.sh` Feel free to read each one and assign perms individually, cause it is your computer :stuck_out_tongue_winking_eye: and security is a real thing.

8. Run the `build.sh` script to build the project. Since you are going to be running it on the local machine you will want to run: `./bin/build.sh -l` - This command is doing a docker-compose build in the background. It is downloading the images needed for the project to your local machine and then building for a local development environment.

9. Once this completes you will now want to start up the project. We will use the start.sh script for this, again using the `-l` flag to run locally:  `./bin/start.sh -l` The first time you run this you will see the database restores. You can ignore the error messages. You will also see the api container start up.

10. Once the first startup completes kill the container using cmd c/ctrl c depending on your os.

11. Restart the container using the same start command:  `./bin/start.sh -l` and both the db and the api will start up.

12. Open your browser and you will be able to access the Django Rest Framework browserable front end at `http://localhost:8000/api`, the Swagger API schema at `http://localhost:8000/schema`, and the Django `admin` login at `http://localhost:8000/admin`.

13. To Run Tests: run the `./bin/build-test.sh -l` command.

## Run in Staging Environment

While developing the API, using the built in dev server is useful as it allows for live reloading, and debug messages. When running in a production environment, this is a security risk, and not efficient. As such a staging/production environment has been created using the following technologies:

* Gunicorn - A "green" HTTP server
* Gevent - Asynchronous workers
* Pyscopgreen - A "green" version of the psycop database connector
* WhiteNoise - allows for hosting of static files by gunicorn in a prod environment vs. integrating a webserver

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

## License

We follow the MIT License: https://github.com/hackoregon/transportation-system-backend/blob/staging/LICENSE

## Contributors

<To Be added>
