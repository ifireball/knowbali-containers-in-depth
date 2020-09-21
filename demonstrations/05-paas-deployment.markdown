DEMO: Deploying an application to a PaaS
========================================

Our test app
------------

We have a Django-based app (The Blog all from Django-girls tutorial).

To get the app source code:

    git clone https://github.com/ifireball/knowbali-containers-in-depth.git

To set up development dependencies:

    cd knowbali-containers-in-depth
    pipenv sync

To run it locally:

    pipenv run python3 manage.py migrate
    pipenv run python3 manage.py runserver 8080

In this command:
* `pipenv` manages the Python virtual environment and takes care of Python
  dependencies for us
* `manage.py` is the Django command-line tool
* We ask the server to run on port 8080 jut to be compatible with the way the
  container images do it, the default is port 8000.

Now we can go to `http://localhost:8080` with a browser and see our site. We
can:
* Log in
* Add posts
* Edit posts
* Delete posts
* Log out

We can do `^C` to stop the server. With `ls -l` we can see the `db.sqlite3`
file.

Heroku
------
[Heroku][1] is a PaaS that offer (limited) free application hosting. It supports
many different programming languages such as Python, ruby, Java, PHP and others.

[1]: https://www.heroku.com

Adapting the app to run on Heroku
---------------------------------

The app may need some adaptations to be compatible with Heroku.

For Django applications, a couple of dependency packages need to be added, some
changes need to be done to `settings.py` and a `Procfile` needs to be added.
Documentation about needed settings can be found [here][2].

[2]: https://devcenter.heroku.com/articles/django-app-configuration

Since Django applications typically use a database and require database
migrations to be configured and run, we need to tell Heroku to do that for us.
[Here][3] is documentation about how to do that, and some details [here][4].

[3]: https://help.heroku.com/GDQ74SU2/django-migrations
[4]: https://devcenter.heroku.com/articles/release-phase#specifying-release-phase-tasks

Running the app on Heroku
-------------------------

We're going to setup automation in Heroku that will download the application
source code directly from GitHub and run it.

Here are the steps to do this:

1. From the Heroku main dashboard, click on "Create new app"
2. Fill-in an app name (Will be used in URL) and a region (In our case -
   `beyond-blog`).
3. From under "Deployment method" choose "GitHub"
4. Click the "Connect to GitHub" button below.
5. In the pop-up window, authorize communications between GitHub and Heroku.
6. In the "Connect to GitHub" section that shows up, search your repository (in
   our case its "ifireball/knowbali-containers-in-depth"), and click on the
   "Connect" button that show up next to it.
7. To deploy right now, select the "master" branch in the "Manual deploy"
   section and click "Deploy Branch". We will see build output logs displayed as
   our app is being deployed. Among other things, the `Pipfile` is read
   automatically, dependencies are installed, a database is created, migrations
   are run and finally the app is brought up.

The app will be available in the following URL:

> https://beyond-blog.herokuapp.com/

We can also setup Heroku to re-deploy the application every time we merge a
patch in GitHub.

7. In the "Automatic deploys" section, choose the branch you want to deploy from
   ("master" for our app) and click "Enable Automatic Deploys" (We leave "Wait
   for CI to pass before deploy" off for now).
