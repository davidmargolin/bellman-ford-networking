import os
import click
from dotenv import load_dotenv
load_dotenv()

@click.command()
@click.argument('query')
def cli_command(query):
    click.echo(query)

if __name__ == "__main__":
    cli_command()