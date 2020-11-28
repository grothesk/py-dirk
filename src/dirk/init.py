import click
import os

from .utils import is_executable
from .files import EnvrcFile, KubeconfigFile


@click.command()
@click.option(
    '-c', '--configfile',
    envvar='DIRK_CONFIGFILE',
    type=click.Path(exists=True)
)
@click.option(
    '-m', '--mode',
    envvar='DIRK_MODE',
    type=click.Choice(['skip', 'replace']),
    default='skip'
)
def init(configfile, mode):
    cwd = os.getcwd()

    click.echo('dirk: init dirk in {cwd}.'.format(cwd=cwd))

    click.echo('dirk: check if direnv is present on PATH.')
    if is_executable('direnv'):
        click.echo('dirk: direnv is on PATH.')

        envrc = EnvrcFile(directory=cwd)
        envrc.process()

        kubeconfig = KubeconfigFile(directory=cwd)
        kubeconfig.process(configfile, mode)
    else:
        click.echo('dirk: cannot find direnv on PATH.')
        click.echo('dirk: please make sure that direnv has been installed.')
