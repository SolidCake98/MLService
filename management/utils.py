import os
import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from env import env

def docker_compose_cmdargs(commands_string=None):
        config = env.get_env_value()
        env.configure_app()

        docker_compose_file = os.path.join("docker", f"{config}.yml")

        if not os.path.isfile(docker_compose_file):
            raise ValueError(f"The file {docker_compose_file} does not exist")

        command_args = [
            "-p",
            env.get_env_value(),
            "-f",
            docker_compose_file,
        ]

        if commands_string:
            command_line.extend(commands_string.split(" "))

        return command_args

def run_sql(statements):
    conn = psycopg2.connect(
        dbname  =os.getenv("POSTGRES_DB"),
        user    =os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host    =os.getenv("POSTGRES_HOSTNAME"),
        port    =os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()
