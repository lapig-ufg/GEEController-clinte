import click
from os import environ
from dynaconf import settings


@click.command()
@click.option(
    '--login', default=0, help='If it is 1 Force Google Earth Engine login.'
)
@click.option(
    '--max_queue',
    default=6,
    help='Define the amount of task that the client can do at the same time, by default it is 6.',
)
@click.option('--run_class', default='all', help='Set Class.')
@click.option('--version', default=settings.VERSION, help='Set version.')
def start(login, max_queue, run_class, version):
    environ['DYNACONF_LOGIN_FORCE'] = str(login)
    environ['DYNACONF_QUANTITY_ALLOWED_IN_QUEUE'] = str(max_queue)
    environ['DYNACONF_CLASS_RUM'] = str(run_class)
    environ['DYNACONF_VERSION'] = str(version)
    from ClientGEE.cliente import main

    main()


if __name__ == '__main__':
    start()
