DEMO: Building with Dockerfiles
===============================

We place the following contents in `wsgi-app/Dockerfile`:

    FROM registry.redhat.io/rhel8/httpd-24

    # Switch to root
    USER 0

    # Doing installation and cleanup in a sinlge command to avoid garbage layers
    RUN \
        yum install -y python3-mod_wsgi && \
        yum clean all

    # Copy the application files (No need to mess with permissions this time)
    COPY myapp.conf /etc/httpd/conf.d/
    COPY myapp.py /var/www/

    # Swtich back to an unprivileged user so the container uses it at runtime
    USER 1001

    # We don't need to secify an entrypoint because we inherit it from the base
    # image

We build the image with the following command:

    docker build wsgi-app -t myapp-df

We can launch a container with our new image using:

    docker run -d --rm --name=myapp -p 8080:8080 myapp-df

Finally lets clean up after ourselves:

    docker kill myapp myapp2
