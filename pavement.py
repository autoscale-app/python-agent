from paver.tasks import task, needs
from paver.easy import sh


@task
@needs(["format", "test"])
def default():
    pass


@task
def check():
    sh("black --check .")


@task
def format():
    sh("black .")


@task
def test():
    sh("pytest")
