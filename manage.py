""" Command Line initdb and dropdb functions for faster devolpment """
import click

from app import create_all, drop_all


@click.group()
def cli():
    pass


@click.command()
def initdb():
    create_all()
    click.echo("Database created")


@click.command()
def dropdb():
    drop_all()
    click.echo("Database dropped")


cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()
