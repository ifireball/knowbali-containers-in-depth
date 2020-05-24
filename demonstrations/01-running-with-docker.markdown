DEMO: Running containers with Docker
====================================

Starting a basic container
--------------------------

We can run a container with a simple command:

    docker run centos:8

It looks like nothing happened lets try to inspect running containers:

    docker ps

Again we don't see anything, but we can also ask for containers that ran in the
past:

    docker ps -a

Ok, now we see something. Our container started and stopped immediately. Why is
that?

Lets try to give our container something to do this time:

    docker run centos:8 sleep inf

This time out shell looks "stuck" because the container is running and doing
nothing. Lets check what is going on in a different window:

    docker ps

We can see our container running now. Lets make note of the randomly allocated
name because we need it for later.

We can "go into" the container by using:

    docker exec -it $CONTAINER_NAME /bin/bash

* The '-i' and '-t' options tell Docker to arrange for interactive applications
  to work

Now inside the container we can run the following to see where we are:

    cat /etc/system-release

We can see the user we're working with:

    whoami

* Notice that we're `root` now inside the container and not the normal user
  account we were using outside
* The user we get by default is determined by settings in the container image
  and we can also change this via Docker options.
* Security tip: `root` inside == `root` outside! Do not let applications run as
  root in production!

We can also use `ps` to see which other processes are running in the container:

    ps -ef

We see:
* The main process of the container running as PID 1 (Who here knows what PID 1
  does in Linux?)
* The shell we are using right now
* The `ps` process we just invoked

We can use `exit` or `^D` to exit the shell inside the container and go back to
our normal machine shell.

We can kill the container with:

    docker kill $CONTAINER_NAME

Now we can see that:
* The shell where we started the container got released
* The container no longer show up in `docker ps`
* We can see the container is with status `Exited` in `docker ps -a`

We can clean up all the dead containers with:

    docker rm $CONTAINER_NAME ...

Using containers as interactive, isolated environments
------------------------------------------------------

So far it was a little cumbersome to work with Docker, we can get a better
experience by running a command like the following:

    docker run -it --rm --name=my_container centos:8

In this command:
* `-i` and `-t` tells Docker to setup interactive communications with the
  process in the container (Just like we did with `docker exec`).
* `--rm` tells Docker to delete the container immediately when it exists
* `--name` assigns a name to the container

Once we run the command:
* We get an interactive shell in the container immediately
* **Note:** The CentOS image runs a shell by default, with other images we may
  need to explicitly ask for `/bin/bash`.
* If we run `ps -ef` we can see our shell in PID 1.
* If we run `docker ps` (In another shell window), we can see the container
  running with the name we gave it
* When we exit the shell the container exits and gets deleted. We can see this
  with `docker ps -a`

Running a service container
---------------------------

Lets run a container with a service application in it:

    docker run -d --rm --name=mysvc -p 8080:8080 registry.redhat.io/rhel8/httpd-24

In this command:
* `-d` makes Docker leave our shell alone
* `--rm` makes Docker delete the container when it exits
* `--name` assign a less-silly name
* `-p` maps a port from the container to `localhost`
* The `http-24` image contains the Apache web server

After we run the command we can use the following to check that the container is
running:

    docker ps

We can now use a browser to access the web server at:

    http://localhost:8080

We will see the RHEL Apache welcome page.

We can see the Apache logs via:

    docker logs mysvc

We can also "tail" the live logs with:

    docker logs -f mysvc

With this command running we can see the log updating when we refresh the
browser window. We use `^C` to stop watching the logs.

Now lets try to make the web server display something else. We'll got into the
container:

    docker exec -it mysvc /bin/bash

Now we can go into `/var/www/html` and create an `index.html` file with the
following content:

    <h1>Hello from container!</h1>

When we refresh the browser we will see the page we just made.

If we kill the container and re-start it, our changes are gone (Why?).

    docker kill mysvc
    docker run -d --rm --name=mysvc -p 8080:8080 registry.redhat.io/rhel8/httpd-24

Finally lets kill this container to leave our machine empty:

    docker kill mysvc

(Can show that the browser no longer connects)
