DEMO: Advanced container building
=================================

Building with quay.io
---------------------

**Note**: We can only use public base images when building in quay.io.
Alternatively we can use private images that are in quay.io private repos by
using a bot account.

Creating the repository:

 1. From the quay.io UI we click on "Create New Repository"
 2. We assign the repository the name: "simpleblog".
 3. We set it for "Public" access.
 4. We select "Link to GitHub Repository Push".
 5. We click "Create Public Repository". If this is the first time we setup a
    link between quay.io and GitHub we may be asked to login to GitHub and
    approve creating the link.

 6. If we have more the one GitHub org - we select the right one.
 7. We select the GitHub repository to link.
 8. We click "Continue"

 9. We select "Trigger for all branches and tags" (For repositories where
    temporary development branches may be stored, we may want to setup a filter
    regex).
10. We click "Continue"

11. We leave the check marks on both "Tag manifests with branch or tag name" and
    "Add latest tag if on default branch".
12. We click continue

13. We select the `Dockerfile.centos` (Continue)
14. And the context `/` (Continue)

15. If all goes well, quay.io will tell us so and show ue the SSH key id added
    to the GitHub repo for cloning the source.
16. We can click on "go back to..." to go back to our repository main screen.

To trigger a build manually:

 1. From the repository screen click on the gear icon on the appropriate line in
    the "Build Triggers" list, and select "Run Trigger Now".
 2. Select the branch we want to build.
 3. We can click on the build number to watch the build log.

Once the build is done we can see the new tag in the "Repository Tags" screen.

Building with s2i
-----------------

**Note**: we need to have the s2i tool installed. We can get it here:

    https://github.com/openshift/source-to-image/releases

To run the build with s2i:

    s2i build . registry.redhat.io/ubi8/python-36 quay.io/bkorren/simpeblog

Note:
* S2i moves file around with Git. We need to commit all changes before running it
* There are various ways to customize the build, depending on the base images.
  In our case we have an `.s2i/environment` file to enable `Pipenv` in the
  image.

We can also generate Dockerfiles with s2i via:

    s2i build . registry.redhat.io/ubi8/python-36 --as-dockerfile Dockerfile.new

Note:
* This creates the `uploads` directory and copies all the files there. It also
  makes the `Dockerfile` assume the files are there so we need to modify it a
  little to make it copy the files from `.`.

