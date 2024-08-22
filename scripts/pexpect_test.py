import pexpect
import sys
import time
import locale
locale.setlocale(locale.LC_CTYPE, 'en_US.ISO8859-15')

session = pexpect.spawn('ssh -o HostkeyAlgorithms=+ssh-rsa corellan@qad.surfrut.com', timeout=5, maxread=10000, env={"TERM": "xterm"})
session.logfile = sys.stdout.buffer

try:
    # Initial login
    session.expect('password:')
    session.sendline('corellan.,.')

    # Selecting QAD Piloto option
    session.expect(b'Ingrese Opci\xf3n: ')
    session.send('2')

    session.write('corellan')
    session.sendcontrol('m')
    session.write('corellan.,.')
    session.sendcontrol('m')
    session.expect(b'Enter data or press F4 to end.')
    print(session.after)

    # session.expect(b'SURFRUSD')
    #session.sendline('')

finally:
    session.close()