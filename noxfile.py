# noxfile.py
import tempfile

import nox

nox.options.sessions = "lint", "safety", "tests"
locations = "folio_uuid", "noxfile.py"


@nox.session()
def tests(session):
    print(session.posargs)
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session()
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session()
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session()
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
