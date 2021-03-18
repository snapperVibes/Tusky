""" Command Line tool for interacting with the server and database """
import click
import uvicorn

from app import create_all, drop_all, init_app

@click.group()
def cli():
    pass


@click.command()
def initdb():
    success = create_all()
    if success:
        click.echo("Tables were created and the super-user was initialized")
    else:
        click.echo("Tables were created")


@click.command()
def dropdb():
    drop_all()
    click.echo("Database dropped")


@click.command()
def resetdb():
    drop_all()
    create_all()
    click.echo("Database reset")


@click.command()
def runserver():
    """ Initializes and starts a development server"""
    create_all()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(resetdb)
cli.add_command(runserver)

if __name__ == "__main__":
    cli()
