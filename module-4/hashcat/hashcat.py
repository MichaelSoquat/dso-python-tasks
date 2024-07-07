import argparse
import itertools
import string
import hashlib

parser = argparse.ArgumentParser(description='Hashcat implementation in Python', add_help=False)
parser.add_argument('-m', required=True, type=int, choices=[0, 1, 2, 3], help='Hashmode: MD5 (0), SHA-1 (1), SHA-256 (2), und SHA-512 (3)')
parser.add_argument('-a', required=True, type=int, choices=[0, 1], help='Attackmode: Brute-Force Attack (0), Dictionary Attack (1)')
parser.add_argument('-h', type=str, help='Hashstring for brute force or dictionary attack')
parser.add_argument('-H', type=str, help='File containing hashstring for brute force or dictionary attack')
parser.add_argument('--help', action='help', help='Show this help message and exit')

args = parser.parse_args()

# Check if we have valid arguments, exactly one of -h or -H must be specified
if bool(args.h) ^ bool(args.H):
    print('Valid arguments provided')
else:
    parser.error('-h or -H must be specified')

def hash_password(password, hash_func):
    hasher = hash_func()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()

def hack_password(passwordlist, hash_to_find):
    hash_functions = {
        0: hashlib.md5,
        1: hashlib.sha1,
        2: hashlib.sha256,
        3: hashlib.sha512
    }
    hash_func = hash_functions[args.m]
    
    for password in passwordlist:
        password = password.strip()
        hashed_password = hash_password(password, hash_func)
        print(password, hashed_password)
        if hashed_password == hash_to_find:
            print(f'The password is: {password}')
            return
    print('Password not found')

# Determine the hash to find
if args.h:
    hash_to_find = args.h
else:
    try:
        with open(args.H, 'r', encoding='utf-8', errors='ignore') as passwordfile:
            hash_to_find = passwordfile.read().strip()
    except FileNotFoundError:
        print(f'File {args.H} not found')
        exit()

# Brute-Force Attack
if args.a == 0:
    max_password_length = 8  # Maximum length for passwords
    character_set = string.ascii_letters + string.digits
    
    for length in range(6, max_password_length + 1):
        password_combinations = itertools.product(character_set, repeat=length)
        
        hack_password(map(''.join, password_combinations), hash_to_find)

# Dictionary Attack
elif args.a == 1:
    try:
        with open('./rockyou.txt', 'r', encoding='utf-8', errors='ignore') as file:
            passwordlist = file.readlines()
            hack_password(passwordlist, hash_to_find)
    except FileNotFoundError:
        print('File rockyou.txt not found')


# abc123 sha 256
# 0123456789 sha 512