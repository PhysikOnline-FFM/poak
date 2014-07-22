from fabric.api import local, lcd

def prepare_deployment(branch_name):
    local('python manage.py test poak')
    local('git add -p && git commit')

def deploy():
    with lcd('/home/poak/poak/'):
        local('git pull')
