import subprocess
import signal
import os
import time
import psycopg2

from abc import ABC, abstractmethod
from env import env
from management.utils import docker_compose_cmdargs, run_sql


class ConsoleCommand(ABC):
    """
    Интерфейс Консольной команды для ее выполнения
    """

    @abstractmethod
    def execute(self):
        pass

class SimpleConsoleCommand(ConsoleCommand):
    """
    Общее обьявление конслоьной команды
    """

    def __init__(self, command:str, *args):
        self.command = command
        self.subcommand = list(args)

    def execute(self):
        env.configure_app()
        cmdline = [self.command] + self.subcommand
        try:
            p = subprocess.Popen(cmdline)
            p.wait()

        except KeyboardInterrupt:
            p.send_signal(signal.SIGINT)
            p.wait() 
        

class TestCommand(ConsoleCommand):
    """
    Команда для запуска тестов
    """
    
    def __init__(self, *args):
        self.args = list(args)


    def wait_for_logs(self, cmdline: list, message: str):
        logs = subprocess.check_output(cmdline)
        while message not in logs.decode("utf-8"):
            logs = subprocess.check_output(cmdline)
            time.sleep(0.1)

    def execute(self):
        env.set_app_env("testing")
        env.configure_app()
        docker_cmd = ["docker-compose"] + docker_compose_cmdargs()

        cmdline = docker_cmd + ["up", "-d"]
        subprocess.call(cmdline)

        cmdline = docker_cmd + ["logs", "db"]

        self.wait_for_logs(cmdline, "ready to accept connections")
        time.sleep(1)

        run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

        cmdline = ["pytest", "-svv", "--cov=application", "--cov-report=term-missing"]
        cmdline.extend(self.args)
        subprocess.call(cmdline)

        cmdline = docker_cmd + ["down"]
        subprocess.call(cmdline)


class InitialDBCommand(ConsoleCommand):
    """
    Команда инициализации базы данных
    """
    
    def execute(self):
        env.configure_app()

        try:
            run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
        except psycopg2.errors.lookup('42P04'):
            print(
                f"Databse {os.getenv('APPLICATION_DB')} already exist and will not be recreated"
            )
        
        