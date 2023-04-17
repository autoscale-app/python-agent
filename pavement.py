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
    sh("coverage run -m pytest")


@task
def coverage_report():
    sh("coverage report")


@task
def coverage_html():
    sh("coverage html")
    sh("open htmlcov/index.html")
