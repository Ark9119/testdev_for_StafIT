from pathlib import Path
import subprocess
import sys
import tempfile


def test_cli_help():
    '''Тест вывода справки.'''
    result = subprocess.run(
        [sys.executable, '-m', 'main', '--help'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert '--files' in result.stdout
    assert '--report' in result.stdout


def test_cli_invalid_report():
    '''Тест ошибки при неверном типе отчёта.'''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv') as f:
        f.write('country,gdp\nUSA,100\n')
        f.flush()

        result = subprocess.run(
            [
                sys.executable, '-m', 'main',
                '--files', f.name,
                '--report', 'non-existent'
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 1
        assert (
            'не поддерживается' in result.stderr
            or 'non-existent' in result.stdout
        )
