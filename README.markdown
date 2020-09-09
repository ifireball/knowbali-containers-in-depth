Containers-in-Depth demonstrations
==================================

This projects include code and notes used in the demonstrations shown during the
"Containers-in-Depth" lecture given as part of the "Open Source development"
course.

The slides for the lecture could be found [in Google Docs][1.1].

[1.1]: https://docs.google.com/presentation/d/1OndiX0m4qNk7LvtUVliRG2TvZJH5b2vqsLeVifbSdSc/edit#slide=id.g547716335e_0_260

What can I find here
--------------------

* This repository mostly consists of a *Django* web application used to
  demonstrate running a moderately-complex application in a container. This
  application is the same one developed when one works on the
  [Django Girls tutorial][2.1].
* This repository also contains Dockerfiles, Ansible playbooks, Vagrantfiles and
  other files used to demonstrate how to build and run the application container
  in various ways.
* The `wsgi-app` directory contains a tiny Python web app used in demonstrations
  where using a fully fledged app would be cumbersome.
* Finally, the `demonstrations` directory contains notes used when giving the
  actual demonstrations in class.

[2.1]: https://tutorial.djangogirls.org/en/

Prerequisites for following along
---------------------------------

The demonstrations had been designed to allow students to follow along on their
own machines in class. Doing so, however requires some tools to be installed on
the students' computers before going into class.

Following is a list of the required tools ans settings:

1. [Docker][3.1] absolutely must be installed and ready for use in order to
   follow any of the demonstrations. There are ways to install Docker on Windows
   or MAC, but since students had issues with this in the past I now recommend
   setting up a Linux VM with VirtualBox or Vagrant and installing the Docker
   package there.
2. To practice pushing images to remote registries, you need a [quay.io][3.7]
   account. You can create one [here][3.8], or simply sign-in with your existing
   Google or GitHub accounts
3. To run the [Django][3.9] test application locally, as well as
   [Docker compose][3.10] and [Ansible][3.11], you need to have:
   1. [Python][3.12] (3.6.8 or newer). Installation instructions can be found
      [here for Windows][3.13] and [here for Mac][3.14]. For Linux you should
      install Python 3.6.8 or newer using your package manager
   2. [Pipenv][3.15]. Instructions for installing it are [here][3.16], but
      please don't bother trying to use Homebrew if you're not using a Mac.
      Instead, either use `pip` with the `--user` option (`pip` should be
      included with your Python installation), or use [Pipx][3.17] followig
      the instructions [here][3.18].
4. If you want to try running [S2i][3.19] locally, you can download it
   [here][3.20] and simply extract the single file you will find in the archive
   suitable for your OS to some location that is pointed to by `$PATH`
5. To run the [Vagrant][3.21]-based demonstrations follow the instructions
   [here][3.22] to install it. You'll also need [VirtualBox][3.23] (Instructions
   [here][3.24], but if you're usine Windows, please see the [note below](#vn))
   or, alternatively if using Linux, you can use the
   [vagrant-libvirt][3.25] plugin to use the native virtualization system
   (Installation instruction are in the main `README.md` file)

This list of tools may seem extensive, but most of these are standard tools
you'll find on any developer's workstation. The major tools have been used in
other parts of the course already, so they are hopefully already installed on
most students` computers.

[3.1]: https://www.docker.com/
[3.7]: https://quay.io/
[3.8]: https://quay.io/signin/
[3.9]: https://www.djangoproject.com/
[3.10]: https://docs.docker.com/compose/
[3.11]: https://www.ansible.com/
[3.12]: https://www.python.org/
[3.13]: https://www.python.org/downloads/windows/
[3.14]: https://www.python.org/downloads/mac-osx/
[3.15]: https://pipenv.pypa.io/en/latest/
[3.16]: https://pipenv.pypa.io/en/latest/install/#installing-pipenv
[3.17]: https://pipxproject.github.io/pipx/
[3.18]: https://pipxproject.github.io/pipx/installation/
[3.19]: https://github.com/openshift/source-to-image
[3.20]: https://github.com/openshift/source-to-image/releases
[3.21]: https://www.vagrantup.com/
[3.22]: https://www.vagrantup.com/docs/installation/
[3.23]: https://www.virtualbox.org/
[3.24]: https://www.virtualbox.org/wiki/Downloads
[3.25]: https://github.com/vagrant-libvirt/vagrant-libvirt
[3.26]: https://www.vagrantup.com/docs/hyperv/
[3.27]: https://stackoverflow.com/a/38111013/8243700
