#! /usr/bin/env python

import os
import json
import signal
import subprocess
import click
from env import env

from management.commands import ConsoleCommand, SimpleConsoleCommand, TestCommand, InitialDBCommand
from management.utils import docker_compose_cmdargs


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    command: ConsoleCommand = SimpleConsoleCommand('flask',*subcommand)
    command.execute()
    

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    command: ConsoleCommand = SimpleConsoleCommand('docker-compose', *docker_compose_cmdargs(), *subcommand)
    command.execute()

@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
    command : Command = TestCommand(*filenames)
    command.execute()

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def migrate(subcommand):
    command = SimpleConsoleCommand("alembic", *subcommand)
    command.execute()

@cli.command()
def create_initial_db():
    command = InitialDBCommand()
    command.execute()


if __name__ == "__main__":
    cli()