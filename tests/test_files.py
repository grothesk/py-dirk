from pathlib import Path
import os

from dirk.files import BaseFile, EnvrcFile, KubeconfigFile
from dirk.settings import EXPORT_KUBECONFIG


def test_base_file(tmp_path):
    base_file = BaseFile(directory=tmp_path)
    assert not base_file.exists()

    envrc_file = tmp_path / BaseFile.filename
    envrc_file.touch()
    assert base_file.exists()


def test_envrc_file_process(tmp_path):
    envrc_file = EnvrcFile(directory=tmp_path)
    assert not envrc_file.exists()

    # If there is no .envrc,
    envrc_file.process()
    assert envrc_file.exists()
    p = Path(envrc_file.path)
    assert p.read_text() == '{export}\n'.format(export=EXPORT_KUBECONFIG)

    # If .envrc does not contain 'export KUBECONFIG='
    p.write_text('test')
    envrc_file.process()
    with p.open() as f:
        lines = f.readlines()
    assert lines[-1] == '{export}\n'.format(export=EXPORT_KUBECONFIG)

    # If KUBECONFIG is not set properly
    p.write_text('test\nexport KUBECONFIG="test"\ntest')
    envrc_file.process()
    with p.open() as f:
        lines = f.readlines()
    assert lines[-2] == '{export}\n'.format(export=EXPORT_KUBECONFIG)

    # If KUBECONFIG is already set properly
    p.write_text('test\n{export}\ntest'.format(export=EXPORT_KUBECONFIG))
    envrc_file.process()
    with p.open() as f:
        lines = f.readlines()
    assert lines[-2] == '{export}\n'.format(export=EXPORT_KUBECONFIG)


def test_kubeconfig_file_process(tmp_path):
    kubeconfig_file = KubeconfigFile(directory=tmp_path)
    p = Path(kubeconfig_file.path)

    configfile = os.path.join(tmp_path, 'config')
    p_config = Path(configfile)
    p_config.write_text('config')

    # If there is no kubeconfig in the directory
    assert not kubeconfig_file.exists()

    # If there is no kubeconfig in the directory
    kubeconfig_file.process(configfile=None, mode='skip')
    assert kubeconfig_file.exists()
    assert p.read_text() == ''
    assert oct(os.stat(kubeconfig_file.path).st_mode & 0o777) == '0o600'

    # If there is a kubeconfig in the directory
    p.write_text('test')
    kubeconfig_file.process(configfile=None, mode='skip')
    assert p.read_text() == 'test'

    # If there is a kubeconfig in the directory
    os.chmod(kubeconfig_file.path, 0o666)
    kubeconfig_file.process(configfile=None, mode='replace')
    assert p.read_text() == ''
    assert oct(os.stat(kubeconfig_file.path).st_mode & 0o777) == '0o600'

    # If there is a kubeconfig in the directory
    os.chmod(kubeconfig_file.path, 0o666)
    kubeconfig_file.process(configfile=configfile, mode='replace')
    assert p.read_text() == 'config'
    assert oct(os.stat(kubeconfig_file.path).st_mode & 0o777) == '0o600'

    # If there is a kubeconfig in the directory
    p.write_text('test')
    kubeconfig_file.process(configfile=configfile, mode='skip')
    assert p.read_text() == 'test'

    # If there is no kubeconfig in the directory
    os.remove(kubeconfig_file.path)
    kubeconfig_file.process(configfile=configfile, mode='replace')
    assert p.read_text() == 'config'
    assert oct(os.stat(kubeconfig_file.path).st_mode & 0o777) == '0o600'
