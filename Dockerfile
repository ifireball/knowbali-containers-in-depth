FROM registry.access.redhat.io/ubi8/python-36
LABEL "io.openshift.s2i.build.source-location"="/home/bkorren/src/github.com/ifireball/knowbali-containers-in-depth/." \
      "io.k8s.display-name"="quay.io/bkorren/django-blog" \
      "io.openshift.s2i.build.image"="registry.redhat.io/ubi8/python-36" \
      "io.openshift.s2i.build.commit.author"="Barak Korren <bkorren@redhat.com>" \
      "io.openshift.s2i.build.commit.date"="Sat May 23 01:14:46 2020 +0300" \
      "io.openshift.s2i.build.commit.id"="01cdc8bbe81d5303d3370884818fd1094311cdd0" \
      "io.openshift.s2i.build.commit.ref"="master" \
      "io.openshift.s2i.build.commit.message"="Add Postgres support to blog app"
ENV ENABLE_PIPENV="true"
USER root
# Copying in source code
COPY . /tmp/src
# Change file ownership to the assemble user. Builder image must support chown command.
RUN chown -R 1001:0 /tmp/src
USER 1001
# Assemble script sourced from builder image based on user input or image metadata.
# If this file does not exist in the image, the build will fail.
RUN /usr/libexec/s2i/assemble
# Run script sourced from builder image based on user input or image metadata.
# If this file does not exist in the image, the build will fail.
CMD /usr/libexec/s2i/run
