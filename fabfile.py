import os

from fabric.api import run, cd
from fabric.contrib.console import confirm
from fabric.decorators import hosts

PROJECT_DIR = os.path.dirname(__file__)


@hosts('asimo@xchange.asimo.webfactional.com')
def deploy_production():
    if confirm('This action will deploy to the site xchange.asimo.webfactional.com, are you sure?', default=True):

        with cd('/home/asimo/webapps/xchange_flask/xchange/'):
            run('git pull')
            run('pip-2.7 install -r requirements.txt', pty=True)


        with cd('/home/asimo/webapps/xchange_flask/'):
            run('apache2/bin/restart')