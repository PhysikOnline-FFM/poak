poak
====

(version for django1.6)

## development

### setup

to develop on your own machine do the following:

install `virtualenvwrapper`:
````
sudo pip install virtualenvwrapper
````

create a new file (e.g. `env_variables.sh`) with the content:
````
export WORKON_HOME=$HOME/.virtualenv
export PROJECT_HOME=$HOME/directory-you-do-development-in
source /usr/local/bin/virtualenvwrapper.sh
````

include the file in your current shell session:
````
. env_variables.sh
````

create a virtual environment
````
mkvirtualenv your-project-name
````

go to your development directory and clone this repository
````
git clone https://github.com/PhysikOnline-FFM/poak.git
````

go into the cloned project and install the required packages:
````
pip install -r requirements.txt
````

leave the virtual environment:
````
deactivate
````

### working

before you can start the virtual environment, you always need to include the
environment variables
````
. env_variables.sh
````

after that type
````
workon your-project-name
````
and you're again inside the virtual environment

to leave, type
````
deactivate
````
