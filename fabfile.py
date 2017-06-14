from fabric.api import local, settings, abort
from fabric.contrib.console import confirm


def test():
    with settings(warn_only=True):
        result = local('nosetests -v', capture=True)
    if result.failed and not confirm('Tests failed. Continue?'):
        abort('Aborted at user request.')


def commit():
    message = input('Enter a git commit message: ')
    local(f"git add . && git commit -am '{message}'")


def push():
    local('git branch')
    branch = input('Which branch do you want to push to? ')
    local(f'git push origin {branch}')


def prepare():
    test()
    commit()
    push()


# deploy


def pull():
    local('git pull origin master')


def heroku():
    local('git push heroku master')


def heroku_test():
    local('heroku run nosetests -v')


def deploy():
    test()
    heroku()
    heroku_test()


# rollback


def rollback():
    local('heroku rollback')
