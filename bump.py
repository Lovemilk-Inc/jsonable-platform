import sys
from datetime import datetime
from subprocess import call, PIPE, DEVNULL, Popen

process = Popen(['poetry', 'version', '-s'], stdout=PIPE, stderr=DEVNULL)
stdout, _ = process.communicate()

assert process.returncode == 0, f'poetry exited with non-zero return code (got {process.returncode})'


version = tuple(map(int, stdout.decode().strip().split('.')))


if len(version) > 3:
    version = version[:3]

version += (datetime.now().strftime('%Y%m%d%H%M%S'), )

code = call(['poetry', 'version', '.'.join(map(str, version))])
assert code == 0, f'poetry exited with non-zero return code (got {code})'

args = tuple(map(lambda s: s.lower(), sys.argv[1:]))
if '--publish' in args:
    code = call(['poetry', 'publish', '--build'])
    assert code == 0, f'poetry exited with non-zero return code (got {code})'
