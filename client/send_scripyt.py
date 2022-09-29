import click
from dynaconf import settings
from requests import post


@click.command()
@click.option('--file', help='File name.')
@click.option('--version', help='Set version.')
def main(file, version):
    try:
        with open(file, 'r') as f:
            string = f.read()
        data = {
            "version": version,
            "code":string
        }
        p = post(f"{settings.SERVER}/coder/send?key={settings.KEYAPI}",json=data)
        print(p)
    except Exception as e:
        print(f'error: {e}')

if __name__ == '__main__':
    main()
    