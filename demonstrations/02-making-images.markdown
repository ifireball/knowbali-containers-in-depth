DEMO: Making container images
=============================

We're going to make an image that includes a very simple Python WSGI app that
runs on Apache (We're using Python instead of a static page just to get an
indication that the app is running in the container)

The WSGI app source code can be found in the `wsgi-app/` directory along with a
configuration file for Apache to run it.

We start the HTTPD container like we did before:

    docker run -d --name=mysvc -p 8080:8080 centos/httpd-24-centos8

* This time we do not include the `--rm` option so we can still have access to
  the container image after we kill the container.

We go into the container while explicitly requesting to use the `root` user so
we can have permissions to change it:

    docker exec -it -u root  mysvc /bin/bash

We can now install the `mod_wsgi` package:

    yum install -y python3-mod_wsgi

Its a good idea to clean the temporary installation files so the don't end up in
the final installation image:

    yum clean all

We will now copy the app and configuration files into the container (From
another window):

    docker cp wsgi-app/myapp.conf mysvc:/tmp
    docker cp wsgi-app/myapp.py mysvc:/tmp

We will now copy the file to the right locations inside the container and verify
that they get the right permissions:

    ls -l /tmp
    cp -v /tmp/myapp.conf /etc/httpd/conf.d/
    cp -v /tmp/myapp.py /var/www/
    ls -l /var/www/myapp.py /etc/httpd/conf.d/myapp.conf
    rm -fv /tmp/myapp.*

We also need to make Apache reload its configuration so that `mod_wsgi` is
activated, and the app is loaded. We can do this with:

    kill -SIGUSR1 1

**Note:** This does not kill the apache process, it just sends it a signal.

After doing we can see a line like the following in the Apache (container) logs:

    AH00493: SIGUSR1 received.  Doing graceful restart

We can now see the app running in our container by going with a web browser to:

    http://localhost:8080/

Now we can exit our `docker exec` session and kill the container:

    docker kill mysvc

Since we did not use `--rm` we still have the container, and more importantly,
the container temporary layer.

    docker ps -a

We can now commit the layer to turn it into a reusable image:

    docker commit mysvc myapp

We can see the image we've just created with:

    docker images myapp

Now we can try to run a new container using the image we just made:

    docker run -d --rm --name=myapp -p 8080:8080 myapp

And we can run it again on another port!

    docker run -d --rm --name=myapp -p 8081:8080 myapp

We can access both containers with the browser and see different instances of
our app running. We can also see the containers in `docker ps`.

Finally lets clean up after ourselves:

    docker kill myapp myapp2
