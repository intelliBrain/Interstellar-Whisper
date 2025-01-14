#!/usr/bin/python3

'''
Usage:
  whisper.py (-r [-n N] | -s MSG -a ADDR) [-k FILE] [-e ENC]
  whisper.py -h | --help
  whisper.py -v | --version

Options:
  -r            Read messages.
  -s MSG        The message text to send.
  -a ADDR       The destination address (required for sending).
  -n N          Read last N messages (optional for reading) [default: 1].
  -k FILE       Path to the file containing the password-protected stellar
                seed for your account [default: ~/.stellar/wallet].
  -e ENC        Required encoding for the message text [default: 0].
                Valid options are:
                  0 = raw (no) encoding,
                  1 = GSM 03.38 encoding,
                  2 = Sixbit ASCII encoding,
                  3 = smaz compression.
  -v --version  Display version and exit.
  -h --help     Show this screen.
'''
from docopt import docopt
import wallet
from getpass import getpass
import textwrap

# stellar-base
from stellar_base.address import Address
from stellar_base.keypair import Keypair
from stellar_base.utils import StellarMnemonic
# Stellar Whisper
from whisperer import Whisperer


def banner():
    banner = """\
    ____  .   __            .    __       ___         .
 . /  _/___  / /____ *__________/ /____  / / /___ ______ +  /\\
   / // __ \/ __/ _ \/ ___/ ___/ __/ _ \/ / / __ `/ ___/  .'  '.
 _/ // / / / /_/  __/ /  (__  ) /_/  __/ / / /_/ / /     /======\\
/___/_/ /_____/\___/_/  /____/\__/\___/_/_/\__,_/_/     ;:.  _   ;
| |   . / / /_  (_)________  ___  _____                 |:. (_)  |
| | /| / / __ \/ / ___/ __ \/ _ \/ ___/            +    ;:.      ;
| |/ |/ / / / / (__  ) /_/ /  __/ /                   .' \:.XLM / `.
|__/|__/_/ /_/_/____/ .___/\___/_/     .        .    / .-'':._.'`-. \\
                   /_/                               |/    /||\    \|"""
    print(banner)


if __name__ == '__main__':

    banner()

    #sender
    #Public Key
    #GCHI3PNOQAHQIL6L6TALNM33LOYQ7HBZKGZZTRTQSHBNDHCXL6S6PYBE
    #Secret Key
    #SDRJON4EOLUJDTTPAESQYTU67VEQR7RBPYRFWZELLK3YJ5GKJHIYOYZM

    sender_secret ='SDRJON4EOLUJDTTPAESQYTU67VEQR7RBPYRFWZELLK3YJ5GKJHIYOYZM'
    receiver_secret = ''


    alice_secret: 'SC7G2Y4DAGF3ARCEDGYYW4CR7E3RSOCDHMOLRRWOOWSIUILIOED6DLDV'
    alice_public: 'GCU2RRJHYBEIP6R6SJHLTCC32FVFGATYMTYB3ZBKT3OMPZLCTVSS7ZDH'

    bob_secret: 'SDVYV44C63H4S6W4FT4SBNML3C4YNUA75Z4DZBDP6OBBEZUREBMP3KIP'
    bob_public: 'GD2TA2JCQTM6ILRQB2JL3GIZSUKHVU5MDJSHRLM7VMNORLT6SZB72TIY'

    # Get cmdline arguments
    arguments = docopt(__doc__, version = 'Interstellar Whisper 0.1')

    # Load seed and kreate keypair
    try:
        # password = getpass('Enter password: ')
        password='aaaa1111'
    except KeyboardInterrupt:
        print()
        exit(-1)
    seed = wallet.LoadWallet(arguments.get('-k'), password)
    if seed == None:
        exit(-1)

    # Create a Whisperer instance
    kp = Keypair.from_seed(seed)
    #kp = Keypair.from_seed(sender_secret)

    print('\nsecret: {}', kp.seed())

    W = Whisperer(kp)

    # Parse arguments
    if arguments.get('-r'):

        # Read last n messages
        n = int(arguments.get('-n'))
        msg = W.Read(tail = n, printable = False)

        # Display messages
        print('\033[4m' + '                                                                     ' + '\033[0m')
        print('\033[4m' + 'Date        From            Message                                  ' + '\033[0m')
        for i in range(0, len(msg)):
          msgparts = textwrap.wrap(msg[i][2].decode('utf-8', errors = 'ignore'), 41) #[msg[i][2][j:j+41] for j in range(0, len(msg[i][2]), 41)]
          print('{:<10}  {:<12}…   {}'.format(msg[i][0][0:10], msg[i][1][0:12], msgparts[0]))
          for m in msgparts[1:]:
            print('                            {}'.format(m))

    elif arguments.get('-s') is not None:
        # Check if message is provided
        msg = arguments.get('-s')

        #Check if receiving address is provided
        address = arguments.get('-a')
        if not Whisperer.ValidateAddress(address):
            print('\nError: No valid Stellar destination address provided!')
            exit(-1)

        print('\nSending message to {}...\t'.format(address), end = '')
        W.Send(address, msg.encode(), int(arguments.get('-e')))
        print('Done.')
