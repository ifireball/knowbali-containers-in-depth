DEMO: Sharing container images
==============================

Logging-in to the container registry
------------------------------------

Container images are shared but uploading them into a container registry.

Since a container registry is a remote service we must first create an account
for it and log-in before we can use it. For example, we can create an account on
the *quay.io* registry here:

    https://quay.io/signin/

Once we've signed-in we can go into "Account Settings" to have a `docker login`
command with an encrypted password be generated for us.

Tagging images for upload
-------------------------

Lets have a look at the images we've built so far:

    docker image list | grep myapp

To push an image we need to tag it with the name of the registry and the account
we're going to push into. We can do this directly at build time or we can do
this later with `docker tag`:

    docker tag myapp-df quay.io/bkorren/myapp-df:v1.0

Notes:
* It a good idea to add a version label. IF we don't the image gets tagged as
  the latest.

Now we can see the tag we've just added:

    docker image list | grep myapp

* We can see in the output that the image ID is the same for the name we used
  for building and the name we added right now.

Uploading the image
-------------------

To upload we use `docker push`:

    docker push quay.io/bkorren/myapp-df:v1.0

We can now see the image and its tags in the quay.io UI.

**Note:** By default quay.io sets the image as private. We need to go into
"settings" to make it public, otherwise it'll warn us that we need to upgrade
our account.

To test that we've uploaded successfully, lets first erase all copies of the
image from our local machine:

    docker image rm myapp myapp-df quay.io/bkorren/myapp-df:v1.0

We can now see there are no more copies of the image:

    docker image list | grep myapp

Its worth mentioning that Docker has a command for erasing unused images and
layers:

    docker image prune

When we're convinces we've erased the image lets just try to run a container
with it again, but this time we user the full image name from the registry:

    docker run -d --rm --name=myapp -p 8080:8080 quay.io/bkorren/myapp-df:v1.0

We can see the image being pulled as the container is started.

We can also see we have the mage in our local image store now:

    docker image list | grep myapp
