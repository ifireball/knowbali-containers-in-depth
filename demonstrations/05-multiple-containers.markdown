DEMO: Running multiple containers
=================================

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

Running the app in a container
------------------------------

We wrote a `Dockerfile` for our app (We actually auto-generated it, more about
this later), and we've already built the image for it, so we can simply run it:

    docker run -it --rm -p 8080:8080 quay.io/bkorren/simpleblog

In this command:
* We use `-it --rm` to see the output of the container and delete it
  automatically when doing `^C`.

We can see in the container output that the DB migrations are being run when it
starts up - Why is that?

When we go to `http://localhost:8080` we see our app running, but this time the
Blog is empty - why is that?

Lets add some posts.

If we do `^C` and then rerun the container with:

    docker run -it --rm -p 8080:8080 quay.io/bkorren/simpleblog

We see:
* The DB migrations run again.
* The Blog is empty again.

Why is that?

Using a DB container
--------------------

We're going to run a PostreSQL database in a container and have out app connect
to it and store data in it.

To make this work we need to be able to:
1. Tell Postgres which DB schema to create, and which user accounts.
2. Make the DB container port accessible from the app container
2. Tell our application container how to connect to the DB

We can use environment variables to pass information into the containers and we
can use other Docker options to setup communications between the containers, but
doing this manually with `docker run` commands is cumbersome and error-prone, so
we should use automation tools for this.

Starting up containers with `docker-compose`
--------------------------------------------

Docker compose is a simple tool for automating Docker configuration. It is
written in Python so we can install it via `pip`. In our case we've already set
it up in our `Pipenv` environment.

    pipenv run docker-compose --help

To use Docker compose, we need to write a `docker-compose.yml` file. Lets look
at the one we wrote for our app:

    vim docker-compose.yml

We can see in this file:
- A section for setting up our DB container
- A section for setting up the app container. We can see that we also have
  instructions for building it there, and `docker-compose` will build it for us
  if needed.
- The environment variables we pass to each container
- Port settings for the containers
- Volume settings to place the DB data in permanent storage.

Its important to note that Docker compose automatically sets up connectivity
between the containers, so we don't need to worry about it.

Now we can start our Db container with:

    pipenv run docker-compose up -d db

* The `-d` options is just like with Docker - so the container runs in the
  background and we maintain access to our shell.

Docker compose has similar commands to Docker:

    pipenv run docker-compose ps
    pipenv run docker-compose logs db

We can also see our container with the usual Docker commands:

    docker ps

* We can see docker compose had set it up with a rather long name...

Now lets start our app container:

    pipenv run docker-compose up -d app

And look at the logs:

    pipenv run docker-compose logs app

* We can see the migrations are not being run this time, because I've already
  setup the database in advance.

We can now go into our app at `http://localhost:8080` - We can see we already
have some post there. Lets login and add some more.

Now lets go into the database and see if our posts are actually there:

    pipenv run docker-compose exec db psql simpleblog

In the `psql` prompt:
* We can see all the Django tables with `\d`.
* Lets query our `blog_post` table:

        select * from blog_post;

* We exit the `psql` shell with `^D` or `\q`.

Finally, to shut down the containers that Docker compose started:

    pipenv run docker-compose down

We can also ask docker-compose to start everything at once:

    pipenv run docker-compose up

We can see that our app crashes immediately when we try this (Why?). We have a
race condition where the app is trying to connect to the database before it is
available for use.

Sine we ran `docker-compose` without `-d` this time we can type `^C` to stop it
and shut down all the running containers.

Starting up containers with Ansible
-----------------------------------

When working with Ansible we write *Playbooks* that contain tasks for Ansible to
perform. Ansible task employ Ansible modules that know how to do the actual
work. Lets have a look at the playbook we wrote for starting up out app
containers:

    vim playbooks/start.yaml

In this playbook we can see:
1. A task setting up a data volume for out database
2. A task for starting up the database
3. A task for building the app container
4. A task for waiting for the database to start up (This solves the race
   condition we had when we used Docker compose)
5. (Finally) A task for starting up the app container

Note: Since we can control the exact sequence of operations, we can utilize the
time we wait for the DB to start for building the app container.

Out approach for connecting containers with Ansible is a little different then
what Docker compose did. Instead of using Docker network trick we simply make
Ansible check what is the IP that the DB container has got once it started up
and we simply pass that directly as the DB address to the app container.

Lets run this playbook (Ansible is a Python tool and is already installed in our
pipenv):

    pipenv run ansible-playbook playbooks/start.yaml

We can see in the output that Ansible only makes changes when needed. In this
case it skipped building the container image and creating the volume.

Now we can access our app at `http://localhost:8080`.

To shut-down the containers we have a separate playbook:

    vim playbooks/stop.yaml

We can run it with:

    pipenv run ansible-playbook playbooks/stop.yaml

Starting up containers with Vagrant
-----------------------------------

We're using the Vagrant Docker *provisioner* to run containers on our Vagrant
VM. Lets have a look at the Vagrantfile:

    vim Vagrantfile

We can see it:
1. Starts up the DB container
2. Builds the app container image
3. Runs the app container

Note:
* We use the legacy Docker `--link` option to connect the containers to one
  another because we cannot control Docker networks (Like Docker compose does)
  nor can we query the settings of running containers (Like we did with
  Ansible).
* We use CentOs-based container images instead of RHEL simply to avoid having to
  configure acces to the Red Hat registry in the Vagrant VM.

To start up evetything we use the usual Vagrant command:

    vagrant up

We can shut down everything in the usual way:

    vagrant halt
