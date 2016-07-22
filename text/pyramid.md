pyramid.md

Tutorial Index
  http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/index.html

# Starter Tutorial

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/scaffolds.html  
======================================================================================

Prelude: Quick Project Startup with Scaffolds
---------------------------------------------

  pcreate --list

  cd ~/Desktop/vagrant/dash
  vagrant ...

  /vagrant/code/scaffolds
  pcreate --scaffold starter scaffolds
  cd scaffolds

  - Hack
  sudo chmod 777 /opt/python2/lib/python2.7/site-packages
  sudo chmod 777 /opt/python2/bin

  python setup.py develop

  - Start server
  pserve development.ini --reload

  - Open in browser
  http://localhost:6543

# Check host connection

Inside guest

  curl http://localhost:8080/hello/world

At host

  curl -v http://localhost:8089/hello/world
