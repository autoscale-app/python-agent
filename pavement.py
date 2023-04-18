from paver.easy import sh
from paver.tasks import needs, task


@task
@needs(["format", "test"])
def default():
    pass


@task
def check():
    sh("isort --check . && black --check .")


@task
def format():
    sh("isort . && black .")


@task
def test():
    sh("coverage run -m pytest -vv")


@task
def coverage_report():
    sh("coverage report")


@task
def coverage_html():
    sh("coverage html")
    sh("open htmlcov/index.html")
