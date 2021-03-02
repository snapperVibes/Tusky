""" Command Line initdb and dropdb functions for faster devolpment """
import click

from app import Base, engine

metadata = Base.metadata

@click.group()
def cli():
    pass


@click.command()
def initdb():
    metadata.create_all(engine)
    click.echo("Database created 👍")


@click.command()
def dropdb():
    metadata.drop_all(engine)
    click.echo("Database dropped.")


cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == '__main__':
   cli()
