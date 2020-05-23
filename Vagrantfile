# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  config.vm.box_check_update = false

  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # Container provisioning
  config.vm.provision "docker" do |d|
    # Run DB container, wer'e using the CentOs-based image in order to avoid
    # having to setup credentials for the RedHat registry on the Vagrant VM
    d.run 'db',
      image: 'docker.io/centos/postgresql-96-centos7',
      args: %w'
        -e POSTGRESQL_USER=simpleblog
        -e POSTGRESQL_PASSWORD=simpleblog
        -e POSTGRESQL_DATABASE=simpleblog
        -v "/var/lib/pgsql/data"
        -p 5432:5432
      '.join(' ')

    d.build_image "/vagrant/", args: '-t simpleblog -f /vagrant/Dockerfile.centos'

    d.run 'app',
      image: 'simpleblog',
      args: %w'
        -e DJANGO_DB_BACKEND=psql
        -e POSTGRESQL_HOST=db
        -e POSTGRESQL_PORT=5432
        -e POSTGRESQL_USER=simpleblog
        -e POSTGRESQL_PASSWORD=simpleblog
        -e POSTGRESQL_DATABASE=simpleblog
        -p 8080:8080
        --link db
      '.join(' ')
  end
end
