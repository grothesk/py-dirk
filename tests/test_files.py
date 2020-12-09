from pathlib import Path

from dirk.files import BaseFile, EnvrcFile
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

    # If there does not exist an .envrc,
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
